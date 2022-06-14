pub mod client {
    use serde::{Serialize, Deserialize};
    use serde_json::{self, Error};

    #[derive(Serialize, Deserialize, Debug)]
    pub struct DataClient {
        pub name: String,
        pub age: u8
    }
    impl DataClient {
        pub fn from_string(data: String) -> Result<Self, Error> {
            serde_json::from_str(data.as_str())
        }
        pub fn to_string(&self) -> Result<String, Error> {
            serde_json::to_string(self)
        }
    }    
}

pub mod task {
    use serde::{Serialize, Deserialize};
    use serde_json::{self, Error};

    #[derive(Serialize, Deserialize, Debug)]
    pub struct DataTask {
        pub description: String
    }
    impl DataTask {
        pub fn from_string(data: String) -> Result<Self, Error> {
            serde_json::from_str(data.as_str())
        }
        pub fn to_string(&self) -> Result<String, Error> {
            serde_json::to_string(self)
        }
    }

    impl Clone for DataTask {
        fn clone(&self) -> Self {
            Self { description: self.description.clone() }
        }
    }
}

