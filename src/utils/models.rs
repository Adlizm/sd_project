pub mod client {
    use serde::{Serialize, Deserialize};
    use serde_json;

    #[derive(Serialize, Deserialize, Debug)]
    pub struct DataClient {
        pub name: String,
        pub age: u8
    }
    impl DataClient {
        pub fn from_string(data: String) -> Self {
            serde_json::from_str(data.as_str()).unwrap()
        }
        pub fn to_string(&self) -> String {
            serde_json::to_string(self).unwrap()
        }
    }    
}

pub mod task {



}

