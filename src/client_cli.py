import client.interface as task
from others.net import tcp_connect
from others.response import ResponseType

def handle_client(stream):
    while True:
        print('------------- Client Menu -------------')
        print('Commands: create, update, list, delete')
        print('          delete-all, exit')

        option = input()

        if option == 'create':
            res = task.create(stream)
        elif option == 'update':
            res = task.update(stream)
        elif option == 'list':
            res = task.list(stream)
        elif option == 'delete':
            res = task.delete(stream)
        elif option == 'delete-all':
            res = task.delete_all(stream)
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
        handle_client(stream)
    else:
        print('Cannot connect on client portal')

main()