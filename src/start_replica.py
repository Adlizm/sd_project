import sys
import threading

from others.request import Request, DATA_PAYLOAD

from replica.model import Replica
from replica.net import bind_replica
from replica.config import REPLICAS_SOCKET_ADDRS, REPLICAS_PARAMETERS


lock = threading.Lock()

def handle_portal_requests(stream, client, replica):
    print(f'Connect {client} with sucess! ')
    while True:
        buffer: bytes = stream.recv(DATA_PAYLOAD)
        if not buffer:
            break
        try:
            buffer = buffer.decode('utf-8')
            print(f'Reciving request from {client}! {buffer}')

            request = Request.from_string(buffer)
            response = replica.send(request, sync=True)
            
            print('Response obtained')
            str_response = response.to_string()
            stream.send(bytes(str_response, 'utf-8'))

            print(f'Sending response to {client}! {str_response}')
        except:
            stream.send(b'Cannot make request, try late again')   
    print(f'Disconnect {client} with sucess! ')

def main():
    if len(sys.argv) != 2:
        print("Usage %replica_name \{repl1, repl2, repl3\}")
        return

    replica_name = sys.argv[1]
    tcp = bind_replica(replica_name)
    if not tcp:
        print('Cannot bind replica in a socket')
        return

    host, partners = REPLICAS_PARAMETERS[replica_name]
    replica = Replica(replica_name, host, partners)

    print('Bind concluded with sucess! Waiting for requests...')
    while True:
        stream, client = tcp.accept()
        threading.Thread(target=handle_portal_requests, args=(stream, client, replica)).start()
    
if __name__ == '__main__':
    main()