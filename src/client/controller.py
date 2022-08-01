import sys
import etcd3

sys.path.append('.')

from others.models import DataTask
from others.response import Response, ResponseType
from others.request import Request, RequestType

class TasksController():
    def __init__(self):
        self.data = {}

    def create(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.CreateTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None or req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')
        
        try:
            data_task = DataTask.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))
        
        if etcd.get('/{}'.format(req.cid)) != (None, None):
            if not req.cid in self.data:
                self.data[req.cid] = {}
            if etcd.get('/{}/{}'.format(req.cid, req.task)) == (None, None): 
                self.data[req.cid][req.task] = data_task               #create in cache
                etcd.put('/{}/{}'.format(req.cid, req.task), req.body) #create in etcd
                return Response(ResponseType.Sucess, 'Task created with sucess')

            return Response(ResponseType.Error, 'Task already exist')
        return Response(ResponseType.Error, 'Client id not found')

    def update(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.UpdateTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None or req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        try:
            data_task = DataTask.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        if etcd.get('/{}/{}'.format(req.cid, req.task)) != (None, None):
            if not req.cid in self.data:
                self.data[req.cid] = {}
            etcd.put('/{}/{}'.format(req.cid, req.task), req.body) #update in etcd
            self.data[req.cid][req.task] = data_task               #update in cache
            return Response(ResponseType.Sucess, 'Client updated with sucess')
        return Response(ResponseType.Error, 'Client or task not found')
        
    def list(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.ListTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        list = ''
        if req.cid in self.data: #list from cache
            tasks: dict = self.data[req.cid]
            for name, data in tasks.items():
                list += '\n{} - {}'.format(name, data)
            return Response(ResponseType.Sucess, list)              #list from cache
        elif etcd.get('/{}'.format(req.cid)) != (None, None):
            self.data[req.cid] = {}
            for data, meta in etcd.get_all('/{}/'.format(req.cid)):
                key, value = str(meta.key, encoding='utf-8'), str(data, encoding='utf-8') 
                self.data[req.cid][key] = value
                list += '\n{} - {}'.format(key, value)
            return Response(ResponseType.Sucess, list)              #list from etcd
        return Response(ResponseType.Error, 'Client id not found')
                 
    def delete(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.DeleteTask:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None or req.task == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')
        
        if req.cid in self.data and req.task in self.data[req.cid]: #delete in cache
            del self.data[req.cid][req.task]

        if etcd.delete('/{}/{}'.format(req.cid, req.task)):         #delete in etcd
            return Response(ResponseType.Sucess, 'Task deleted with sucess')
        return Response(ResponseType.Error, 'Client or task not found')
            
    def delete_all(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.DeleteAllTasks:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        if req.cid in self.data:                #delete-all in cache
            self.data[req.cid] = {}
        if etcd.delete_prefix('/{}/'.format(req.cid)): #delete-all in etcd
            return Response(ResponseType.Sucess, 'All tasks deleted with sucess')
        return Response(ResponseType.Error, 'Client not found')

            
        
