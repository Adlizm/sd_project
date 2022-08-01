import sys
import unittest

sys.path.append('./src')

from admin.controller import ClientController
from client.controller import TasksController
from others.response import ResponseType
from others.request import Request, RequestType
from others.models import DataClient, DataTask
from others.etcd import create_client_etcd

class TestClientController(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.controller = ClientController()
        self.etcd = create_client_etcd()

    def test_create(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = self.controller.create(request, self.etcd)
        cid = int(response.data[33::])

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(cid, self.controller.data)
        self.assertEqual(self.controller.data[cid].to_string(), data)

    def test_update(self):
        data = DataClient(name='Boby', age=18)
        request = Request(RequestType.CreateClient, None, None, data.to_string())

        response = self.controller.create(request, self.etcd)
        cid = int(response.data[33::])
        
        data.name = 'Cody'
        data.age = 42
        request = Request(RequestType.UpdateClient, cid, None, data.to_string())
        response = self.controller.update(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertEqual(self.controller.data[cid].name, 'Cody')
        self.assertEqual(self.controller.data[cid].age, 42)
    
    def test_get(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = self.controller.create(request, self.etcd)
        cid = int(response.data[33::])

        request = Request(RequestType.GetClient, cid, None, None)
        response = self.controller.get(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertEqual(response.data, data)

    def test_delete(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)

        response = self.controller.create(request, self.etcd)
        cid = int(response.data[33::])

        request = Request(RequestType.DeleteClient, cid, None, None)
        response = self.controller.delete(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertNotIn(cid, self.controller.data)

class TestTaskController(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.controller = TasksController()
        self.etcd = create_client_etcd()

        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)
        client_controller = ClientController()
        response = client_controller.create(request, self.etcd)

        self.cid = int(response.data[33:])
    
    def test_json_converter(self):
        data = DataTask(description="task of math").to_string()
        self.assertEqual(data, "{\"description\": \"task of math\"}")

    def test_create(self):
        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, self.cid, "homework", data)
        response = self.controller.create(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(self.cid, self.controller.data)
        self.assertIn("homework", self.controller.data[self.cid])
        self.assertEqual(self.controller.data[self.cid]["homework"].description, "task of math")

    def test_update(self):
        data = DataTask(description="task of math")
        request = Request(RequestType.CreateTask, self.cid, "homework", data.to_string())
        response = self.controller.create(request, self.etcd)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)

        data.description = "task of history"
        request = Request(RequestType.UpdateTask, self.cid, "homework", data.to_string())
        response = self.controller.update(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(self.cid, self.controller.data)
        self.assertIn("homework", self.controller.data[self.cid])
        self.assertEqual(self.controller.data[self.cid]["homework"].description, "task of history")

    def test_delete(self):
        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, self.cid, "homework", data)
        response = self.controller.create(request, self.etcd)

        request = Request(RequestType.DeleteTask, self.cid, "homework", None)
        response = self.controller.delete(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(self.cid, self.controller.data)
        self.assertNotIn("homework", self.controller.data[self.cid])

    def test_delete_all(self):
        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, self.cid, "homework1", data)
        response = self.controller.create(request, self.etcd)

        data = DataTask(description="task of histoy").to_string()
        request = Request(RequestType.CreateTask, self.cid, "homework2", data)
        response = self.controller.create(request, self.etcd)

        request = Request(RequestType.DeleteAllTasks, self.cid, None, None)
        response = self.controller.delete_all(request, self.etcd)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(self.cid, self.controller.data)
        self.assertNotIn("homework1", self.controller.data[self.cid])
        self.assertNotIn("homework2", self.controller.data[self.cid])

if __name__ == '__main__':
    unittest.main()