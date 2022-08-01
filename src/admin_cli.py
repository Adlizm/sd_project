import admin.interface as client
from others.net import tcp_connect
from others.response import ResponseType

def handle_admin(stream):
    while True:
        print('------------- Admin Menu -------------')
        print('Commands: create, update, get, delete,')
        print('          exit')

        option = input()

        if option == 'create':
            res = client.create(stream)
        elif option == 'update':
            res = client.update(stream)
        elif option == 'get':
            res = client.get(stream)
        elif option == 'delete':
            res = client.delete(stream)
        elif option == 'exit':
            break
        else:
            continue
        
        if res.status == ResponseType.Sucess:
            print(res.data),
        else:
            print(f'Error: {res.data}')
       

def main():
    stream = tcp_connect()
    if stream:
        handle_admin(stream)
    else:
        print('Cannot connect on admin portal')

main()