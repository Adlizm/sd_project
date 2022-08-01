import sys
import etcd3

sys.path.append('.')

from others.models import DataClient
from others.response import Response, ResponseType
from others.request import Request, RequestType

class ClientController():
    def __init__(self):
        self.data = {}
    
    def create(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.CreateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')
        
        try:
            data_client = DataClient.from_string(req.body)  
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        cid = abs(hash(req.body))
        while etcd.get('/{}'.format(cid)) != (None, None):
            cid += 1

        self.data[cid] = data_client                               # create in cache
        etcd.put('/{}'.format(cid), str(req.body).encode('utf-8')) # create in etcd
        return Response(ResponseType.Sucess, f'Client created with sucess! Cid: {cid}')

    def update(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.UpdateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None or req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        try:
            data_client = DataClient.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        if etcd.get('/{}'.format(req.cid)) != (None, None):
            self.data[req.cid] = data_client               # update in cache
            etcd.put('/{}'.format(req.cid), req.body)      # update in etcd
            return Response(ResponseType.Sucess, 'Client updated with sucess')
        return Response(ResponseType.Error, 'Client not found')

    def get(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.GetClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        # try get from cache
        if req.cid in self.data:
            data_client = self.data[req.cid]                # get from cache
            return Response(ResponseType.Sucess, DataClient.to_string(data_client))
        
        # try get from etcd
        value, _ = etcd.get('/{}'.format(req.cid))
        if value:
            value = str(value, encoding='utf-8')
            self.data[req.cid] = value
            return Response(ResponseType.Sucess, value)
        return Response(ResponseType.Error, 'Client not found')

    def delete(self, req: Request, etcd: etcd3.Etcd3Client) -> Response:
        if req.req != RequestType.DeleteClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        if isinstance(etcd, etcd3.Etcd3Client):
            return Response(ResponseType.Error, 'Invalid client etcd')

        if req.cid in self.data:
            del self.data[req.cid]              # delete in cache
        if etcd.delete('/{}'.format(req.cid)):  # delete in etcd
            return Response(ResponseType.Sucess, 'Client deleted with sucess');
        return Response(ResponseType.Error, 'Client not found')
