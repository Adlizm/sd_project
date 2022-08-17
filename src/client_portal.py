import threading

from others.request import Request, RequestType, DATA_PAYLOAD
from others.response import Response, ResponseType
from others.pubsub import connect_mqtt
from others.net import bind_one, portal_client_addrs 
from client.controller import TasksController

lock = threading.Lock()

def handle_client(stream, client, controller, mqtt):
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
                res = controller.create(req)
            elif req.req == RequestType.UpdateTask:
                res = controller.update(req)
            elif req.req == RequestType.ListTasks:
                res = controller.list(req)
            elif req.req == RequestType.DeleteTask:
                res = controller.delete(req)
            elif req.req == RequestType.DeleteAllTasks:
                res = controller.delete_all(req)
            else:
                res = Response(ResponseType.Error, 'Invalid command received, try connect to client portal!')
        
        str_response = res.to_string()
        print(f'Sending response to {client}: \n{str_response}')
        
        stream.send(bytes(str_response, 'utf-8'))
        if res.status == ResponseType.Sucess:
            topic = topic_from_request(req.req)
            if topic:
                print('Publishing request on broker')
                mqtt.publish(topic, buffer)

    print(f'Disconnect {client} with sucess! ')

def topic_from_request(req) -> str:
    match = {
        RequestType.CreateTask: 'task/create',
        RequestType.UpdateTask: 'task/update',
        RequestType.DeleteTask: 'task/delete',
        RequestType.DeleteAllTasks: 'task/delete-all',
    }
    if req in match:
        return match[req]
    return None

def subscriber(mqtt, controller):
    mqtt.subscribe('client/create')
    mqtt.subscribe('client/delete')
    mqtt.subscribe('task/create')
    mqtt.subscribe('task/update')
    mqtt.subscribe('task/delete')
    mqtt.subscribe('task/delete-all')

    def on_message(client, userdata, msg):
        print(f'Reciving menssage from broker in topic: {msg.topic}')
        data = msg.payload.decode()
        print(data)
        
        request = Request.from_string(data)
        with lock:
            if msg.topic == 'client/create':
                res = controller.new_client(request.cid)
            elif msg.topic == 'client/delete':
                res = controller.delete_client(request.cid)
            elif msg.topic == 'task/create':
                res = controller.create(request)
            elif msg.topic == 'task/update':
                res = controller.update(request)
            elif msg.topic == 'task/delete':
                res = controller.delete(request)
            elif msg.topic == 'task/delete-all':
                res = controller.delete_all(request)
            print(res.data)

    mqtt.on_message = on_message

def main():
    controller = TasksController()
    tcp = bind_one(portal_client_addrs())
    if not tcp:
        print('Cannot bind a client portal')
        return

    mqtt = connect_mqtt(f'client:{str(tcp.getsockname())}')
    subscriber(mqtt, controller)

    mqtt.loop_start()

    print('Bind concluded with sucess! Waiting for requests...')
    while True:
        con, cliente = tcp.accept()
        threading.Thread(target=handle_client, args=(con, cliente, controller, mqtt)).start()

main()
