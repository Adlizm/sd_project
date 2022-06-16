use std::io::stdin;

use crate::utils::models::{client::DataClient, task::DataTask};

pub const USE_CID: u8 = 0x01;
pub const USE_TASK: u8 = 0x02;
pub const USE_BODY: u8 = 0x04;

type OString = Option<String>;

fn get_input(input_name: &str) -> String {
    let mut buffer = String::new();
    
    print!("\n\t{}:", input_name);
    stdin().read_line(&mut buffer).unwrap();

    buffer
}

pub fn get(mask: u8) -> (OString, OString, OString) {
    let mut cid: OString = None;
    let mut task: OString = None;
    let mut body: OString = None;

    if(mask & USE_CID) != 0 {
        cid = Some(get_input("cid"));
    }
    if(mask & USE_TASK) != 0 {
        task = Some(get_input("task name:"));
    }
    if(mask & USE_BODY) != 0 {
        print!("\n\tbody: ");
        if(mask & USE_TASK) != 0 {  
            //task data on body
            let description = get_input(" description:");

            let data = DataTask{description}.to_string().unwrap();
            body = Some(data);
        }else { 
            //client data on body
            let name = get_input(" name:");
            let age = get_input(" age:").parse::<u8>().unwrap();

            let data = DataClient{name, age}.to_string().unwrap();
            body = Some(data);
        }   
    }
    (cid, task, body)
}

