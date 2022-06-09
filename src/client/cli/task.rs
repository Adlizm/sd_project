use std::net::TcpStream;

use sd_project::utils::request::{RequestType, make_request};
use sd_project::utils::response::Response;
use sd_project::utils::inputs::{USE_CID, USE_TASK, USE_BODY};

pub fn create(stream: &TcpStream) -> Response {
	make_request(stream, RequestType::CreateTask, USE_CID|USE_TASK|USE_BODY)
}
pub fn update(stream: &TcpStream)-> Response {
	make_request(stream, RequestType::UpdateTask, USE_CID|USE_TASK|USE_BODY)
}
pub fn list(stream: &TcpStream) -> Response{
	make_request(stream, RequestType::ListTasks, USE_CID)
}
pub fn delete(stream: &TcpStream) -> Response{
	make_request(stream, RequestType::DeleteTask, USE_CID|USE_TASK)
}
pub fn delete_all(stream: &TcpStream) -> Response{
	make_request(stream, RequestType::DeleteAllTasks, USE_CID)
}

