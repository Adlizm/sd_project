use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Mutex, Arc};
use std::thread;

use mosquitto_client::Mosquitto;

use controller::ClientController;
use sd_project::utils::{config, response::Response};
use sd_project::utils::request::{Request, RequestType};

pub mod controller;

fn handle_admin(mut stream: &TcpStream, controller: Arc<Mutex<ClientController>>, mqtt: &Mosquitto) {
    println!("Connect {:?} with sucess! ", stream.local_addr());
    loop {
        let mut buf = String::new();

        match stream.read_to_string(&mut buf) {
            Ok(n) => {
                if n == 0 { break; }
                let req = Request::from_string(buf);

                let res = match req.req {
                    RequestType::CreateClient => controller.lock().unwrap().create(&req),
                    RequestType::UpdateClient => controller.lock().unwrap().update(&req),
                    RequestType::DeleteClient => controller.lock().unwrap().delete(&req),
                    RequestType::GetClient => controller.lock().unwrap().get(&req),

                    _ => Response::Error("Invalid command received, try connect to admin portal!".to_string())
                };

                if let Response::Sucess(_) = res {
                    match stream.write(res.to_string().as_bytes()) {
                        Err(e) => panic!("{}", e.to_string()),
                        Ok(_) => {
                            println!("Response sent with sucess!")
                        },
                    }

                    let payload = req.to_string();
                    if let Ok(topic) = topic_from_request(req) {
                        mqtt.publish(topic, payload.as_bytes(), 0, false).unwrap();
                    }
                }
            }
            Err(e) =>  panic!("{}", e.to_string())
        }
    }
    println!("Disconnect {:?} with sucess! ", stream.local_addr());
}

fn topic_from_request(req: Request) -> Result<&'static str, &'static str> {
    match req.req {
        RequestType::CreateClient => Ok("client/create"),
        RequestType::UpdateClient => Ok("client/update"),
        RequestType::DeleteClient => Ok("client/delete"),
        _ => Err("This request not has a topic")
    }
}

fn main () {
    let controller = Arc::new(Mutex::new(ClientController::new()));
    let listener = TcpListener::bind(config::portal_client_addrs().as_slice()).unwrap();
        
    let pubsub_addr = config::pubsub_addr();
    let m = mosquitto_client::Mosquitto::new("admin");
    m.connect(pubsub_addr.0, pubsub_addr.1).unwrap();

    m.subscribe("client/create", 0).unwrap();
    m.subscribe("client/update", 0).unwrap();
    m.subscribe("client/delete", 0).unwrap();

    let mut mc = m.callbacks(());
    mc.on_message(|_, msg| {
        if ! msg.retained() {
            let req = Request::from_string(msg.text().to_string());
            match msg.topic() {
                "client/create" => { controller.lock().unwrap().create(&req); },
                "client/update" => { controller.lock().unwrap().create(&req); },
                "client/delete" => { controller.lock().unwrap().delete(&req); },
                _ => todo!()
            }
        }
    });

    for result in listener.incoming() {
        if let Ok(stream) = result {
            let controller = Arc::clone(&controller);
            let mqtt = m.clone();

            thread::spawn( move || { handle_admin(&stream, controller, &mqtt)});
        }
    }
}