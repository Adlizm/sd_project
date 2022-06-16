use num_bigint::BigUint;
use num_traits::identities::{Zero, One};
use std::collections::HashMap;

use sd_project::utils::models::client::DataClient;
use sd_project::utils::request::Request;
use sd_project::utils::response::Response;

pub struct ClientController {
    data: HashMap<String, DataClient>,
    clients: BigUint
}
    
impl ClientController {
    pub fn new() -> Self {
        Self {
            data: HashMap::new(),
            clients: BigUint::zero()
        }
    }

    pub fn create(&mut self, req: &Request) -> Response {
        if req.body == None {
            return Response::Error("Incomplet argumets".to_string());
        }

        let data = req.body.as_ref().unwrap();
        match DataClient::from_string(data.to_string()) {
            Ok(data) => {
                let cid = self.clients.to_string();
                self.data.insert(self.clients.to_string(), data);

                self.clients += BigUint::one();

                return Response::Sucess(format!("Client created with sucess! \n CID: {}", cid).to_string());
            },
            Err(e) => Response::Error(e.to_string())
        }
    }

    pub fn update(&mut self, req: &Request) -> Response {
        if req.cid == None || req.body == None {
            return Response::Error("Incomplet argumets".to_string());
        }

        let cid = req.cid.as_ref().unwrap();
        if self.data.contains_key(cid) {
            let data = req.body.as_ref().unwrap();
            match DataClient::from_string(data.to_string()) {
                Ok(data) => {
                    self.data.insert(cid.to_string(), data);
                    return Response::Sucess("Client updated with sucess!".to_string());
                },
                Err(e) => {
                    return Response::Error(e.to_string());
                }
            }
        }
        return Response::Error("Client not found".to_string());
    }

    pub fn get(&mut self, req: &Request) -> Response {
        if req.cid == None{
            return Response::Error("Incomplet argumets".to_string());
        }

        let cid = req.cid.as_ref().unwrap();
        if self.data.contains_key(cid) {
            let data = self.data.get(cid).unwrap();

            match DataClient::to_string(data) {
                Ok(data) => {
                    return Response::Sucess(data);
                },    
                Err(e) => {
                    return Response::Error(e.to_string());
                }
            }
        }
        return Response::Error("Client not found".to_string());
    }

    pub fn delete(&mut self, req: &Request) -> Response {
        if req.cid == None{
            return Response::Error("Incomplet argumets".to_string());
        }

        let cid = req.cid.as_ref().unwrap();
        if self.data.contains_key(cid) {
            self.data.remove(cid);
            return Response::Sucess("Cliet deleted with sucess".to_string());
        }
        return Response::Error("Client not found".to_string())
    }
}