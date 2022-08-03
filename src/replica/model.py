import sys
import plyvel

sys.path.append('.')

from admin.controller import ClientController
from client.controller import TasksController
from others.request import Request, RequestType

from pysyncobj import SyncObj, SyncObjConf, replicated

class Replica(SyncObj):
    def __init__(self, name, addrs, partners):
        super(Replica, self).__init__(addrs, partners)

        self.__db = plyvel.DB(f'./tmp/{name}/', create_if_missing=True)
        self.__client_controller = ClientController(self.__db)
        self.__task_controller = TasksController(self.__db)

    @replicated
    def send(self, request):
        print('Replica recived request')
        RESQUEST_FUNCTIONS = {
            RequestType.CreateClient: self.__client_controller.create,
            RequestType.UpdateClient: self.__client_controller.update,
            RequestType.GetClient: self.__client_controller.get,
            RequestType.DeleteClient: self.__client_controller.delete,

            RequestType.CreateTask: self.__task_controller.create,
            RequestType.UpdateTask: self.__task_controller.update,
            RequestType.ListTasks: self.__task_controller.list,
            RequestType.DeleteTask: self.__task_controller.delete,
            RequestType.DeleteAllTasks: self.__task_controller.delete_all,
        }
        if request.req in RESQUEST_FUNCTIONS:
            response =  RESQUEST_FUNCTIONS[request.req](request)
            return response
        else:
            return Response(RequestType.Error, 'Invalid request type')