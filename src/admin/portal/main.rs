use std::net::{TcpListener, TcpStream};

use sd_project::utils::config;


fn handle_admin(mut stream: &TcpStream) {
      
}

fn main () {
    let listener = TcpListener::bind(
        config::portal_admin_addrs().as_slice()).unwrap();
        
    for result in listener.incoming() {
        if let Ok(stream) = result {
            handle_admin(&stream);
        }
    }
}