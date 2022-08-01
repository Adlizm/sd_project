import threading
from others.etcd import create_client_etcd

from others.request import Request, RequestType, DATA_PAYLOAD
from others.response import Response, ResponseType
from others.net import  tcp_bind 
from client.controller import TasksController

lock = threading.Lock()

def handle_client(stream, client, controller, etcd_client):
    print(f'Connect {client} with sucess! ')
    while True:
        buffer: bytes = stream.recv(DATA_PAYLOAD)
        if not buffer:
            break
        
        buffer = buffer.decode('utf-8')
        print(f'Resived request from {client}: \n{buffer}')

        req = Request.from_string(buffer)
        with lock:
            if req.req == RequestType.CreateTask:
                res = controller.create(req, etcd_client)
            elif req.req == RequestType.UpdateTask:
                res = controller.update(req, etcd_client)
            elif req.req == RequestType.ListTasks:
                res = controller.list(req, etcd_client)
            elif req.req == RequestType.DeleteTask:
                res = controller.delete(req, etcd_client)
            elif req.req == RequestType.DeleteAllTasks:
                res = controller.delete_all(req, etcd_client)
            else:
                res = Response(ResponseType.Error, 'Invalid command received, try connect to client portal!')
        
        str_response = res.to_string()
        stream.send(bytes(str_response, 'utf-8'))
        print(f'Sending response to {client}: \n{str_response}')

    print(f'Disconnect {client} with sucess! ')

def main():
    etcd_client = create_client_etcd()
    controller = TasksController()
    tcp = tcp_bind()
    if not tcp:
        print('Cannot bind a client portal')
        return

    print('Bind concluded with sucess! Waiting for requests...')
    while True:
        stream, client = tcp.accept()
        threading.Thread(target=handle_client, args=(stream, client, controller, etcd_client)).start()

main()
