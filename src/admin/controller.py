import math
import random

import sys
sys.path.append('.')

from others.models import DataClient
from others.response import Response, ResponseType
from others.request import Request, RequestType

class ClientController():
    DIGITS_BIG_INT = 25
    def __init__(self):
        self.data = {}
    
    def ramdom_cid() -> str:
        final_number = ""
        for _ in range(0, ClientController.DIGITS_BIG_INT):
            final_number += str(math.floor(random.random() * 10))
        return int(final_number)

    def add_client(self, req: Request) -> Response:
        if req.req != RequestType.CreateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None or req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_client = DataClient.from_string(req.body)
            self.data[str(req.cid)] = data_client
            return Response(ResponseType.Sucess, f'Added client {req.cid} with sucess!')

        except Exception as e:
            return Response(ResponseType.Error, str(e))

    def create(self, req: Request) -> Response:
        if req.req != RequestType.CreateClient:
            return Response(ResponseType.Error, 'Invalid Resquest'), None
        if req.body == None:
            return Response(ResponseType.Error, 'Incomplet argumets'), None
        
        try:
            data_client = DataClient.from_string(req.body)
            while True:
                cid = ClientController.ramdom_cid()
                if not (cid in self.data):
                    break

            self.data[cid] = data_client
            return Response(ResponseType.Sucess, f'Client created with sucess! Cid: {cid} '), cid

        except Exception as e:
            return Response(ResponseType.Error, str(e)), None

    def update(self, req: Request) -> Response:
        if req.req != RequestType.UpdateClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.body == None or req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        try:
            data_client = DataClient.from_string(req.body)
            if req.cid in self.data:
                self.data[req.cid] = data_client
            return Response(ResponseType.Sucess, 'Client updeted with sucess')

        except Exception as e:
            return Response(ResponseType.Error, str(e))

    def get(self, req: Request) -> Response:
        if req.req != RequestType.GetClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        
        if req.cid in self.data:
            data_client = self.data[req.cid]
            return Response(ResponseType.Sucess, DataClient.to_string(data_client))
        return Response(ResponseType.Error, 'Client not found')

    def delete(self, req: Request) -> Response:
        if req.req != RequestType.DeleteClient:
            return Response(ResponseType.Error, 'Invalid Resquest')
        if req.cid == None:
            return Response(ResponseType.Error, 'Incomplet argumets')
        
        
        if req.cid in self.data:
            del self.data[req.cid]
            return Response(ResponseType.Sucess, 'Client deleted with sucess');
        return Response(ResponseType.Error, 'Client not found')
