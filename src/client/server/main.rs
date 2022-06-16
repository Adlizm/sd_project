use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Mutex, Arc};
use std::thread;

use mosquitto_client::Mosquitto;

use controller::TasksController;
use sd_project::utils::{config, response::Response};
use sd_project::utils::request::{Request, RequestType};

pub mod controller;

fn handle_client(mut stream: &TcpStream, controller: Arc<Mutex<TasksController>>, mqtt: &Mosquitto) {
    println!("Connect {:?} with sucess! ", stream.local_addr());
    loop {
        let mut buf = String::new();
        
        match stream.read_to_string(&mut buf) {
            Ok(n) => {
                if n == 0 { break; }
                let req = Request::from_string(buf);
                
                let res = match req.req {
                    RequestType::CreateTask => controller.lock().unwrap().create(&req),
                    RequestType::UpdateTask => controller.lock().unwrap().update(&req),
                    RequestType::ListTasks => controller.lock().unwrap().list(&req),
                    RequestType::DeleteTask => controller.lock().unwrap().delete(&req),
                    RequestType::DeleteAllTasks => controller.lock().unwrap().delete_all(&req),
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
                    if let Ok(topic) = request_to_topic(req) {
                        mqtt.publish(topic, payload.as_bytes(), 0, false).unwrap();
                    }
                }
            }
            Err(e) => panic!("{}", e.to_string())
        };       
    }
    println!("Disconnect {:?} with sucess! ", stream.local_addr());
}

fn request_to_topic(req: Request) -> Result<&'static str, &'static str> {
    match req.req {
        RequestType::CreateTask => Ok("task/create"),
        RequestType::UpdateTask => Ok("task/update"),
        RequestType::DeleteTask => Ok("task/delete"),
        RequestType::DeleteAllTasks => Ok("task/delete-all"),
        _ => Err("This request not has a topic")
    }
}

fn main () {
    let controller = Arc::new(Mutex::new(TasksController::new()));
    let listener = TcpListener::bind(config::portal_client_addrs().as_slice()).unwrap();
        
    let pubsub_addr = config::pubsub_addr();
    let m = mosquitto_client::Mosquitto::new("client");
    m.connect(pubsub_addr.0, pubsub_addr.1).unwrap();

    m.subscribe("client/create", 0).unwrap();
    m.subscribe("client/delete", 0).unwrap();
    m.subscribe("task/create", 0).unwrap();
    m.subscribe("task/update", 0).unwrap();
    m.subscribe("task/delete", 0).unwrap();
    m.subscribe("task/delete-all", 0).unwrap();

    let mut mc = m.callbacks(());
    mc.on_message(|_, msg| {
        if ! msg.retained() {
            let req = Request::from_string(msg.text().to_string());
            match msg.topic() {
                "client/create" => { controller.lock().unwrap().new_client(req.cid.unwrap()); },
                "client/delete" => { controller.lock().unwrap().delete_client(req.cid.unwrap()); },
                "task/create" => { controller.lock().unwrap().create(&req); },
                "task/update" => { controller.lock().unwrap().update(&req); },
                "task/delete" => { controller.lock().unwrap().delete(&req); },
                "task/delete-all" => { controller.lock().unwrap().delete_all(&req); },
                _ => todo!()
            }
        }
    });

    for result in listener.incoming() {
        if let Ok(stream) = result {
            let controller = Arc::clone(&controller);
            let mqtt = m.clone();

            thread::spawn( move || { handle_client(&stream, controller, &mqtt)});
        }
    }
}