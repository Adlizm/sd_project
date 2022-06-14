use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

use once_cell::sync::Lazy;
use std::sync::Mutex;

use controller::TasksController;
use sd_project::utils::{config, response::Response};
use sd_project::utils::request::{Request, RequestType};

pub mod controller;

static TASK_TABLE: Lazy<Mutex<TasksController>> = Lazy::new(|| Mutex::new(TasksController::new()));

fn handle_client(mut stream: &TcpStream) {

    println!("Connect {:?} with sucess! ", stream.local_addr());
    loop {
        let mut buf = String::new();
        let res = match stream.read_to_string(&mut buf) {
            Ok(n) => {
                if n == 0 { break; }
                let req = Request::from_string(buf);
                
                match req.req {
                    RequestType::CreateTask => TASK_TABLE.lock().unwrap().create(req),
                    RequestType::UpdateTask => TASK_TABLE.lock().unwrap().update(req),
                    RequestType::ListTasks => TASK_TABLE.lock().unwrap().list(req),
                    RequestType::DeleteTask => TASK_TABLE.lock().unwrap().delete(req),
                    RequestType::DeleteAllTasks => TASK_TABLE.lock().unwrap().delete_all(req),
                    _ => Response::Error("Invalid command received, try connect to admin portal!".to_string())
                }
            }
            Err(e) => Response::Error(e.to_string())
        };
        
        match stream.write(res.to_string().as_bytes()) {
            Err(e) => panic!("{}", e.to_string()),
            Ok(_) => {
                println!("Response sent with sucess!")
            },
        }
        if let Response::Sucess(_) = res {
            

            // publish on pubsub
        }        
    }
    println!("Disconnect {:?} with sucess! ", stream.local_addr());
}

fn main () {

    let listener = TcpListener::bind(
        config::portal_client_addrs().as_slice()).unwrap();
        
    for result in listener.incoming() {
        if let Ok(stream) = result {
            thread::spawn( move || { handle_client(&stream)});
        }
    }
}