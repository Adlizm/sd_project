import threading

from others.request import Request, RequestType, DATA_PAYLOAD
from others.response import Response, ResponseType
from others.pubsub import connect_mqtt
from others.net import bind_one, portal_admin_addrs
from admin.controller import ClientController

lock = threading.Lock()

def handle_admin(stream, client, controller, mqtt):
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
                res, cid = controller.create(req)
            elif req.req == RequestType.UpdateClient:
                res = controller.update(req)
            elif req.req == RequestType.GetClient:
                res = controller.get(req)
            elif req.req == RequestType.DeleteClient:
                res = controller.delete(req)
            else:
                res = Response(ResponseType.Error, 'Invalid command received, try connect to client portal!')
        
        str_response = res.to_string()
        print(f'Sending response to {client}: \n{str_response}')
        
        stream.send(bytes(str_response, 'utf-8'))
        if res.status == ResponseType.Sucess:
            topic = topic_from_request(req.req)
            if topic:
                if(req.req == RequestType.CreateClient):
                    req.cid = cid
                print('Publishing request on broker')
                mqtt.publish(topic, req.to_string())

    print(f'Disconnect {client} with sucess! ')

def topic_from_request(req: RequestType) -> str:
    match = {
        RequestType.CreateClient: 'client/create',
        RequestType.UpdateClient: 'client/update',
        RequestType.DeleteClient: 'client/delete',
    }
    if req in match:
        return match[req]
    return None

def subscriber(mqtt, controller):
    mqtt.subscribe('client/create')
    mqtt.subscribe('client/delete')
    mqtt.subscribe('client/update')

    def on_message(client, userdata, msg):
        print(f'Reciving menssage from broker in topic: {msg.topic}')
        data = msg.payload.decode()
        print(data)
        
        request = Request.from_string(data)
        with lock:
            if msg.topic == 'client/create':
                res = controller.add_client(request)
            elif msg.topic == 'client/update':
                res = controller.update(request)
            elif msg.topic == 'client/delete':
                res = controller.delete(request)
            print(res.data)

    mqtt.on_message = on_message

def main():
    controller = ClientController()
    tcp = bind_one(portal_admin_addrs())
    if not tcp:
        print('Cannot bind a admin portal')
        return


    mqtt = connect_mqtt(f'admin:{str(tcp.getsockname())}')
    subscriber(mqtt, controller)
    mqtt.loop_start()

    print('Bind concluded with sucess! Waiting for requests...')
    while True:
        stream, client = tcp.accept()
        threading.Thread(target=handle_admin, args=(stream, client, controller, mqtt)).start()

main()