import threading
from others.etcd import create_client_etcd

from others.request import Request, RequestType, DATA_PAYLOAD
from others.response import Response, ResponseType
from others.net import tcp_bind
from admin.controller import ClientController

lock = threading.Lock()

def handle_admin(stream, client, controller, etcd_client):
    print(f'Connect {client} with sucess! ')
    while True:
        buffer: bytes = stream.recv(DATA_PAYLOAD)
        if not buffer:
            break
        
        buffer = buffer.decode('utf-8')
        print(f'Resived request from {client}: \n{buffer}')

        req = Request.from_string(buffer)
        with lock:
            if req.req == RequestType.CreateClient:
                res, cid = controller.create(req, etcd_client)
            elif req.req == RequestType.UpdateClient:
                res = controller.update(req, etcd_client)
            elif req.req == RequestType.GetClient:
                res = controller.get(req, etcd_client)
            elif req.req == RequestType.DeleteClient:
                res = controller.delete(req, etcd_client)
            else:
                res = Response(ResponseType.Error, 'Invalid command received, try connect to client portal!')
        
        str_response = res.to_string()
        stream.send(bytes(str_response, 'utf-8'))
        print(f'Sending response to {client}: \n{str_response}')
        
    print(f'Disconnect {client} with sucess! ')

def main():
    etcd_client = create_client_etcd()
    controller = ClientController()
    tcp = tcp_bind()
    if not tcp:
        print('Cannot bind a admin portal')
        return

    print('Bind concluded with sucess! Waiting for requests...')
    while True:
        stream, client = tcp.accept()
        threading.Thread(target=handle_admin, args=(stream, client, controller, etcd_client)).start()

main()