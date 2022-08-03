import sys
import plyvel

sys.path.append('.')

from others.models import DataTask
from others.response import Response, ResponseType
from others.request import Request, RequestType

class TasksController():
    def __init__(self, db):
        self.db = db

    def create(self, req: Request) -> Response:
        if req.req != RequestType.CreateTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None or req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_task = DataTask.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))
        
        cid, task = req.cid, req.task
        if self.db.get(bytes(f'/{cid}', 'utf-8')):
            if not self.db.get(bytes(f'/{cid}/{task}', 'utf-8')):
                try:
                    self.db.put(bytes(f'/{cid}/{task}', 'utf-8'), bytes(req.body, 'utf-8')) #create in db
                    return Response(ResponseType.Sucess, 'Task created with sucess')
                except Exception as e:
                    return Response(ResponseType.Error, str(e))
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

        cid, task = req.cid, req.task
        if self.db.get(bytes(f'/{cid}', 'utf-8')):
            if self.db.get(bytes(f'/{cid}/{task}', 'utf-8')):
                try:
                    self.db.put(bytes(f'/{cid}/{task}', 'utf-8'), bytes(req.body, 'utf-8')) #create in db
                    return Response(ResponseType.Sucess, 'Task created with sucess')
                except Exception as e:
                    return Response(ResponseType.Error, str(e))
            return Response(ResponseType.Error, 'Task not found')
        return Response(ResponseType.Error, 'Client id not found')
        
    def list(self, req: Request) -> Response:
        if req.req != RequestType.ListTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        cid = req.cid
        tasks_list = ''
        if self.db.get('/{}'.format(req.cid)):
            for name, data in self.db.iterator(prefix=bytes(f'/{cid}/', 'utf-8')):
                name, data = str(name, 'utf-8').split('/')[-1], str(data, 'utf-8')
                tasks_list += f'\n{name} - {data}'
            return Response(ResponseType.Sucess, tasks_list)              #list from db
        return Response(ResponseType.Error, 'Client id not found')
                 
    def delete(self, req: Request) -> Response:
        if req.req != RequestType.DeleteTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        cid, task = req.cid, req.task
        try:
            self.db.delete(bytes(f'/{cid}/{task}', 'utf-8'))  #delete in db
            return Response(ResponseType.Sucess, 'Task deleted with sucess')
        except Exception as e:
            return Response(ResponseType.Error, 'Client or task not found')
            
    def delete_all(self, req: Request) -> Response:
        if req.req != RequestType.DeleteAllTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')

        cid = req.cid
        try:
            if self.db.get(bytes(f'/{cid}', 'utf-8')):
                for key, _ in self.db.iterator(prefix=bytes(f'/{cid}/', 'utf-8')):
                    self.db.delete(key)  #delete-all in db
                return Response(ResponseType.Sucess, 'All tasks deleted with sucess')
            return Response(ResponseType.Error, 'Client not found')
        except Exception as e:
            return Response(ResponseType.Error, str(e))
            
        

            
        
