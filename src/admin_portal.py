import threading

from others.cache import Cache
from others.request import Request, RequestType, DATA_PAYLOAD
from others.response import Response, ResponseType
from others.net import tcp_bind
from replica.net import connect_replica

lock = threading.Lock()

def handle_admin(stream, client, replica_stream, cache):
    print(f'Connect {client} with sucess! ')
    while True:
        buffer: bytes = stream.recv(DATA_PAYLOAD)
        if not buffer:
            break
        
        buffer = buffer.decode('utf-8')
        print(f'Resived request from {client}! {buffer}')

        request = Request.from_string(buffer)
        response = None
        if (request.req == RequestType.CreateClient or request.req == RequestType.UpdateClient
            or request.req == RequestType.GetClient or request.req == RequestType.DeleteClient):
            
            with lock:
                if request.req == RequestType.GetClient:
                    response = cache.get(request)

            if not response:
                try:
                    with lock:
                        replica_stream.send(bytes(request.to_string(), 'utf-8'))
                        response = replica_stream.recv(DATA_PAYLOAD)
                        
                        if request.req == RequestType.GetClient:
                            cache.put(request, response)
                except:
                    pass
            if response:
                stream.send(response)
                str_response = str(response, 'utf-8')
                print(f'Sending response to {client}! {str_response}')
        else:
            stream.send(b'Invalid request, try connect on client portal')        

    print(f'Disconnect {client} with sucess! ')

def main():
    tcp = tcp_bind()
    if not tcp:
        print('Cannot bind a admin portal')
        return
    print('Bind concluded with sucess!')

    replica_name = input('Replica name to connect (repl1, repl2, repl3): ')
    replica_stream = connect_replica(replica_name)
    if not replica_stream:
        print('Cannot connect in replica')
        return
    print('Connect in replica with sucess!')

    cache = Cache()
    print('Created local cache!')

    print('Waiting from connections...')
    while True:
        try:
            stream, client = tcp.accept()
            threading.Thread(target=handle_admin, args=(stream, client, replica_stream, cache)).start()
        except:
            pass

main()