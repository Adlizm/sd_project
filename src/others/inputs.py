from .models import DataClient, DataTask

USE_CID = 0x01
USE_TASK = 0x02
USE_BODY = 0x04

def get_input(input_name: str):
    value = input(f'\t{input_name}: ')
    return value

def get(mask: int):
    cid, task, body = None, None, None

    if (mask & USE_CID) != 0:
        cid = int(get_input('cid'))
    
    if(mask & USE_TASK) != 0:
        task = get_input('task name')
    
    if(mask & USE_BODY) != 0:
        print('\n\tbody: ');
        if(mask & USE_TASK) != 0: 
            #task data on body
            description = get_input(' description')

            data = DataTask(description).to_string()
            body = data
        else: 
            #client data on body
            name = get_input(' name')
            age = int(get_input(' age'))

            data = DataClient(name, age).to_string()
            body = data;
          
    return (cid, task, body)


