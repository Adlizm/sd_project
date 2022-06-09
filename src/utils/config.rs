#[derive(Debug)]
pub struct ServerConfig {
    pub host: String,
    pub port: String
}

pub fn server_config() -> ServerConfig {
    ServerConfig {
        host: String::from("localhost"),
        port: String::from("3333")
    }  
}
