use std::{net::TcpStream, io::{Read, Write}};
use serde::{Serialize, Deserialize};
use serde_json;

use super::{inputs, response::Response};

#[derive (Serialize, Deserialize)]
pub enum RequestType{
	CreateTask, UpdateTask, ListTasks, DeleteTask, DeleteAllTasks,
	CreateClient, UpdateClient, GetClient, DeleteClient,
}

#[derive (Serialize, Deserialize)]
pub struct Request {
	pub req: RequestType,
	pub cid: Option<String>,
	pub task: Option<String>,
	pub body: Option<String>
}

impl Request {
    pub fn from_string(data: String) -> Self {
        serde_json::from_str(data.as_str()).unwrap()
    }
    pub fn to_string(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }
}

pub fn make_request(mut stream: &TcpStream, req: RequestType, mask: u8) -> Response {
	let inputs = inputs::get(mask);
	
	let req = Request {
		req,
		cid:  inputs.0,
		task: inputs.1,
		body: inputs.2
	};
	
	match stream.write(req.to_string().as_bytes()) {
		Ok(_) => {},
		Err(e) => {
			return Response::Error(e.to_string()) 
		},
	} 

	let mut res = String::new();
	match stream.read_to_string(&mut res) {
		Ok(_) => Response::from_string(res),
		Err(e) => Response::Error(e.to_string()),
	}
}