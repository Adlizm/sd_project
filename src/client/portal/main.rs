use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

use sd_project::utils::{config, response::Response};
use sd_project::utils::request::{Request, RequestType};

pub mod handlers;

fn handle_request(req: Request) -> Response {
    match req.req {
        RequestType::CreateTask => handlers::create(req),
        RequestType::UpdateTask => handlers::update(req),
        RequestType::ListTasks => handlers::list(req),
        RequestType::DeleteTask => handlers::delete(req),
        RequestType::DeleteAllTasks => handlers::delete_all(req),
        _ => Response::Error("Invalid command received, try connect to admin portal!".to_string())
    }
}

fn handle_client(mut stream: &TcpStream) {
    loop {
        let mut buf = String::new();
        let res = match stream.read_to_string(&mut buf) {
            Ok(n) => {
                if n == 0 { break; }
                
                let req = Request::from_string(buf);
                handle_request(req)
            }
            Err(e) => Response::Error(e.to_string())
        };
        if let Response::Sucess(_) = res {
            // publish on pubsub
        }

        match stream.write(res.to_string().as_bytes()) {
            Err(e) => eprintln!("{}", e.to_string()),
            Ok(_) => println!("Response sent with sucess!"),
        }
    }
}

fn main () {
    let listener = TcpListener::bind(
        config::portal_client_addrs().as_slice()).unwrap();
        
    for result in listener.incoming() {
        if let Ok(stream) = result {
            println!("{:?} has beeb connected! ", stream.local_addr());
            thread::spawn(move || handle_client(&stream));
            println!("Client has been disconnected! ");
        }
    }
}