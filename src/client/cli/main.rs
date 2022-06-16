use std::net::{TcpStream};
use sd_project::utils::response::Response;
use sd_project::utils::config;

pub mod task;

fn handle_client(mut stream: &TcpStream) {
    loop {
        println!("------------- Client Menu -------------");
        println!("Commands: create, update, list, delete");
        println!("          delete-all, exit");

        let mut buf = String::new();
        std::io::stdin().read_line(&mut buf).unwrap();
        
        let res = match buf.trim() {
            "create"    => task::create(&mut stream),
            "update"    => task::update(&mut stream),
            "list"      => task::list(&mut stream),
            "delete"    => task::delete(&mut stream),
            "delete-all"=> task::delete_all(&mut stream),
            "exit"      => break,

            _ => Response::Error("Invalid command".to_string()),
        };
        match res {
            Response::Sucess(s) => println!("{}", s),
            Response::Error(s) => eprintln!("{}", s),
        }
    }    
}

fn main () {
    let stream = TcpStream::connect(
        config::portal_client_addrs().as_slice()).unwrap();
    handle_client(&stream);
}