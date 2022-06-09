use std::net::{TcpStream};
use sd_project::utils::response::Response;

pub mod task;

enum OptionType {
    CreateTask,
    UpdateTask,
    ListTaks,
    DeleteTask,
    DeleteAllTasks,
    Exit
}
fn option_from_string(option: &str) -> Option<OptionType> {
    match option {
        "create" => Some(OptionType::CreateTask),
        "update" => Some(OptionType::UpdateTask),
        "list" => Some(OptionType::ListTaks),
        "delete" => Some(OptionType::DeleteTask),
        "delete-all" => Some(OptionType::DeleteAllTasks),
        "exit" => Some(OptionType::Exit),
        _ => None
    }
}

fn handle_client(mut stream: &TcpStream) {
    loop {
        let mut buf = String::new();
        std::io::stdin().read_line(&mut buf).unwrap();
        
        let res = match option_from_string(buf.trim()) {
            Some(OptionType::CreateTask) => task::create(&mut stream),
            Some(OptionType::UpdateTask) => task::update(&mut stream),
            Some(OptionType::ListTaks) => task::list(&mut stream),
            Some(OptionType::DeleteTask) => task::delete(&mut stream),
            Some(OptionType::DeleteAllTasks) => task::delete_all(&mut stream),
            Some(OptionType::Exit) => break,

            None => Response::Error("Invalid command".to_string()),
        };
        match res {
            Response::Sucess(s) => println!("{}", s),
            Response::Error(s) => eprintln!("{}", s),
        }
    }    
}

fn main () {
    let stream = TcpStream::connect("localhost:4000").unwrap();
    handle_client(&stream);
}