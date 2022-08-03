import sys
import plyvel

sys.path.append('.')

from others.models import DataClient
from others.response import Response, ResponseType
from others.request import Request, RequestType

class ClientController():
    def hashcode(data: str):
        PRIME = 18446744069414584321
        BASE = 5926535897

        acc = 1
        hashcode = 9471413089
        for char in bytes(data, 'utf-8'):
            acc = (acc * BASE) % PRIME
            hashcode = (hashcode + char * acc) % PRIME
        return hashcode

    def __init__(self, db: plyvel.DB):
        self.db = db
    
    def create(self, req: Request) -> Response:
        if req.req != RequestType.CreateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_client = DataClient.from_string(req.body)  
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        cid = ClientController.hashcode(req.body)
        while self.db.get(bytes(f'/{cid}', 'utf-8')) != None:
            cid += 1

        try:
            self.db.put(bytes(f'/{cid}', 'utf-8'), bytes(req.body, 'utf-8'))
            return Response(ResponseType.Sucess, f'Client created with sucess! Cid: {cid}')
        except Exception as e:
            return Response(ResponseType.Error, str(e))

    def update(self, req: Request) -> Response:
        if req.req != RequestType.UpdateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None or req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')

        try:
            data_client = DataClient.from_string(req.body)
        except Exception as e:
            return Response(ResponseType.Error, str(e))

        cid = req.cid
        if self.db.get(bytes(f'/{cid}', 'utf-8')):
            try:
                self.db.put(bytes(f'/{cid}', 'utf-8'), bytes(req.body, 'utf-8'))
                return Response(ResponseType.Sucess, 'Client updated with sucess')
            except Exception as e:
                return Response(ResponseType.Error, str(e))
        return Response(ResponseType.Error, 'Client not found')

    def get(self, req: Request) -> Response:
        if req.req != RequestType.GetClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        cid = req.cid
        value = self.db.get(bytes(f'/{cid}', 'utf-8'))
        if value:
            value = str(value, 'utf-8')
            return Response(ResponseType.Sucess, value)
        return Response(ResponseType.Error, 'Client not found')

    def delete(self, req: Request) -> Response:
        if req.req != RequestType.DeleteClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')

        cid = req.cid                  
        try:
            self.db.delete(bytes(f'/{cid}', 'utf-8'))
            return Response(ResponseType.Sucess, 'Client deleted with sucess')
        except Exception as e:
            return Response(ResponseType.Error, 'Client not found')
