use std::net::{TcpStream};
use sd_project::utils::response::Response;
use sd_project::utils::config;

pub mod client;

fn handle_admin(mut stream: &TcpStream) {
    loop {
        let mut buf = String::new();
        std::io::stdin().read_line(&mut buf).unwrap();
        
        let res = match buf.trim() {
            "create" => client::create(&mut stream),
            "update" => client::update(&mut stream),
            "get"    => client::get(&mut stream),
            "delete" => client::delete(&mut stream),
            "exit"   => break,

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
        config::portal_admin_addrs().as_slice()).unwrap();
    handle_admin(&stream);
}