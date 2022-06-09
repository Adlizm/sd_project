use serde::{Serialize, Deserialize};
use serde_json;

#[derive (Serialize, Deserialize)]
pub enum Response{
	Sucess(String), Error(String)
}

impl Response {
    pub fn from_string(data: String) -> Self {
        serde_json::from_str(data.as_str()).unwrap()
    }
    pub fn to_string(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }
}