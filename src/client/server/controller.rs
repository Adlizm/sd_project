use std::collections::HashMap;

use sd_project::utils::models::task::DataTask;
use sd_project::utils::request::Request;
use sd_project::utils::response::Response;

pub struct TasksController {
    data: HashMap< String, HashMap<String, DataTask>>,
}

impl TasksController {
    pub fn new() -> Self {
        TasksController { 
            data: HashMap::new(),
        }
    }

    pub fn new_client(&mut self, cid: String) {
        self.data.insert(cid, HashMap::new());
    }

    pub fn create(&mut self, req: Request) -> Response {
        if None == req.cid || None == req.task || None == req.body {
            return Response::Error("Incomplet arguments".to_string());
        }
        let cid = req.cid.unwrap();
        let name = req.task.unwrap();
        let body = req.body.unwrap();
        
        if self.data.contains_key(&cid) {
            let tasks_table = self.data.get(&cid).unwrap();

            if !tasks_table.contains_key(&name) {
                match DataTask::from_string(body) {
                    Ok(task) => {
                        self.data.get_mut(&cid).unwrap().insert(name, task);
                        return Response::Sucess("Task created with sucess".to_string());
                    }
                    Err(e) => {
                        return Response::Error(e.to_string()); 
                    }
                }
            }
            return Response::Error("Already existing task".to_string());
        }
        return Response::Error("Client id not found".to_string());
    }

    pub fn update(&mut self, req: Request) -> Response {
        if None == req.cid || None == req.task || None == req.body {
            return Response::Error("Incomplet arguments".to_string());
        }
        let cid = req.cid.unwrap();
        let name = req.task.unwrap();
        let body = req.body.unwrap();
        
        if self.data.contains_key(&cid) {
            let tasks_table = self.data.get(&cid).unwrap();

            if tasks_table.contains_key(&name) {
                match DataTask::from_string(body) {
                    Ok(task) => {
                        self.data.get_mut(&cid).unwrap().insert(name, task);
                        return Response::Sucess("Task created with sucess".to_string());
                    }
                    Err(e) => {
                        return Response::Error(e.to_string()); 
                    }
                }
            }
            return Response::Error("Task not found".to_string());
        }
        return Response::Error("Client id not found".to_string());
    }

    pub fn list(&mut self, req: Request) -> Response {
        if None == req.cid {
            return Response::Error("Incomplet arguments".to_string())
        }
        let cid = req.cid.unwrap();

        if self.data.contains_key(&cid) {
            let tasks = self.data.get(&cid).unwrap().into_iter()
                .map(|(task, data)| { format!("{} - {:?}", task, data)})
                .reduce(|tasks, task| { format!("{}\n{}", tasks, task) });

            let tasks =  if tasks == None { "".to_string() } else { tasks.unwrap().to_string() };
            
            return Response::Sucess(tasks.to_string())
        }
        return Response::Error("Client id not found".to_string())
    }

    pub fn delete(&mut self, req: Request) -> Response {
        if None == req.cid || None == req.task {
            return Response::Error("Incomplet arguments".to_string());
        }
        let cid = req.cid.unwrap();
        let name = req.task.unwrap();
        
        if self.data.contains_key(&cid) {
            let tasks_table = self.data.get(&cid).unwrap();

            if tasks_table.contains_key(&name) {
                self.data.get_mut(&cid).unwrap().remove(&name);
                return Response::Sucess("Task deleted with sucess".to_string());
            }
            return Response::Error("Task not found".to_string())
        }
        return Response::Error("Client id not found".to_string())
    }
    
    pub fn delete_all(&mut self, req: Request) -> Response {
        if None == req.cid {
            return Response::Error("Incomplet arguments".to_string());
        }
        let cid = req.cid.unwrap();
        
        if self.data.contains_key(&cid) {
            self.data.get_mut(&cid).unwrap().clear();
            return Response::Sucess("Tasks deleted with sucess".to_string());
        }
        return Response::Error("Client id not found".to_string());
    }
}

impl Clone for TasksController {
    fn clone(&self) -> Self {
        Self { data: self.data.clone() }
    }
}