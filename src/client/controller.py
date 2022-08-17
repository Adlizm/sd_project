import sys
sys.path.append('.')

from others.models import DataTask
from others.response import Response, ResponseType
from others.request import Request, RequestType

class TasksController():
    def __init__(self):
        self.data = {}

    def new_client(self, cid: int) -> Response:
        self.data[cid] = {}
        return Response(ResponseType.Sucess, f'Added Client {cid} with sucess')

    def delete_client(self, cid: int) -> Response:
        del self.data[cid]
        return Response(ResponseType.Sucess, f'Deleted client {cid} with sucess')

    def create(self, req: Request) -> Response:
        if req.req != RequestType.CreateTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None or req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_task = DataTask.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        if req.cid in self.data:
            if not req.task in self.data[req.cid]:
                self.data[req.cid][req.task] = data_task
                return Response(ResponseType.Sucess, 'Task created with sucess')
            return Response(ResponseType.Error, 'Task already exist')
        return Response(ResponseType.Error, 'Client id not found')

    def update(self, req: Request) -> Response:
        if req.req != RequestType.UpdateTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None or req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_task = DataTask.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        if req.cid in self.data:
            if req.task in self.data[req.cid]:
                self.data[req.cid][req.task] = data_task
                return Response(ResponseType.Sucess, 'Task created with sucess')
            return Response(ResponseType.Error, 'Task not found')
        return Response(ResponseType.Error, 'Client id not found')

    def list(self, req: Request) -> Response:
        if req.req != RequestType.ListTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')

        if req.cid in self.data:
            tasks: dict = self.data[req.cid]
            
            list = ''
            for name, data in tasks.items():
                list += f'\n{name} - {data.to_string()}'

            return Response(ResponseType.Sucess, list)
        return Response(ResponseType.Error, 'Client id not found')

    def delete(self, req: Request) -> Response:
        if req.req != RequestType.DeleteTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        
        if req.cid in self.data:
            if req.task in self.data[req.cid]:
                del self.data[req.cid][req.task]
                return Response(ResponseType.Sucess, 'Task deleted with sucess')
            return Response(ResponseType.Error, 'Task not found')
        return Response(ResponseType.Error, 'Client not found')

    
    def delete_all(self, req: Request) -> Response:
        if req.req != RequestType.DeleteAllTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        
        if req.cid in self.data:
            self.data[req.cid].clear()
            return Response(ResponseType.Sucess, 'All Tasks deleted with sucess')
        return Response(ResponseType.Error, 'Client not found')
