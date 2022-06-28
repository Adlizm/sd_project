use std::net::TcpStream;

use sd_project::utils::request::{RequestType, make_request};
use sd_project::utils::response::Response;
use sd_project::utils::inputs::{USE_CID, USE_BODY};

pub fn create(stream: &TcpStream) -> Response {
	make_request(stream, RequestType::CreateClient, USE_CID|USE_BODY)
}
pub fn update(stream: &TcpStream)-> Response {
	make_request(stream, RequestType::UpdateClient, USE_CID|USE_BODY)
}
pub fn get(stream: &TcpStream) -> Response{
	make_request(stream, RequestType::GetClient, USE_CID)
}
pub fn delete(stream: &TcpStream) -> Response{
	make_request(stream, RequestType::DeleteClient, USE_CID)
}

