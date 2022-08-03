import sys
import unittest

sys.path.append('./src')

from replica.model import Replica
from replica.config import REPLICAS_PARAMETERS

from others.response import ResponseType
from others.request import Request, RequestType
from others.models import DataClient, DataTask


replica = None

class TestClientController(unittest.TestCase):
    def test_json_converter(self):
        data = DataClient(name='Boby', age=18).to_string()
        self.assertEqual(data, "{\"name\": \"Boby\", \"age\": 18}")
    
    def test_create(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

    def test_update(self):
        data = DataClient(name='Boby', age=18)
        request = Request(RequestType.CreateClient, None, None, data.to_string())

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])
        
        data.name = 'Cody'
        data.age = 42
        request = Request(RequestType.UpdateClient, cid, None, data.to_string())
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)
    
    def test_get(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        request = Request(RequestType.GetClient, cid, None, None)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

    def test_delete(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        request = Request(RequestType.DeleteClient, cid, None, None)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

class TestTaskController(unittest.TestCase):    
    def test_json_converter(self):
        data = DataTask(description='task of math').to_string()
        self.assertEqual(data, "{\"description\": \"task of math\"}")

    def test_create(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        data = DataTask(description='task of math').to_string()
        request = Request(RequestType.CreateTask, cid, 'homework', data)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

    def test_update(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        data = DataTask(description='task of math')
        request = Request(RequestType.CreateTask, cid, 'homework', data.to_string())
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        data.description = 'task of history'
        request = Request(RequestType.UpdateTask, cid, 'homework', data.to_string())
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

    def test_delete(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        data = DataTask(description='task of math').to_string()
        request = Request(RequestType.CreateTask, cid, 'homework', data)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        request = Request(RequestType.DeleteTask, cid, 'homework', None)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

    def test_delete_all(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        cid = int(response.data[33::])

        data = DataTask(description='task of math').to_string()
        request = Request(RequestType.CreateTask, cid, "homework1", data)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        data = DataTask(description="task of histoy").to_string()
        request = Request(RequestType.CreateTask, cid, "homework2", data)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        request = Request(RequestType.DeleteAllTasks, cid, None, None)
        response = replica.send(request, sync=True)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)


def main():
    host, partners = REPLICAS_PARAMETERS['tests']

    global replica
    replica = Replica('tests', host, partners)

    if not replica:
        print('Testing is not possible as the replica cannot be accessed')
    else:
        unittest.main()

if __name__ == '__main__':
    main()