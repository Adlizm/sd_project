import sys
import unittest

sys.path.append('./src')

from admin.controller import ClientController
from client.controller import TasksController
from others.response import ResponseType
from others.request import Request, RequestType
from others.models import DataClient, DataTask


class TestClientController(unittest.TestCase):
    def test_json_converter(self):
        data = DataClient(name='Boby', age=18).to_string()
        self.assertEqual(data, "{\"name\": \"Boby\", \"age\": 18}")

    def test_add_client(self):
        cid, data = "1231", DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, cid, None, data)
        controller = ClientController()

        response = controller.add_client(request)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(cid, controller.data)
        self.assertEqual(controller.data[cid].to_string(), data)

    def test_create(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)
        controller = ClientController()

        response, cid = controller.create(request)
        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(cid, controller.data)
        self.assertEqual(controller.data[cid].to_string(), data)

    def test_update(self):
        data = DataClient(name='Boby', age=18)
        request = Request(RequestType.CreateClient, None, None, data.to_string())
        controller = ClientController()

        _, cid = controller.create(request)
        data.name = 'Cody'
        data.age = 42
        request = Request(RequestType.UpdateClient, cid, None, data.to_string())
        response = controller.update(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertEqual(controller.data[cid].name, 'Cody')
        self.assertEqual(controller.data[cid].age, 42)
    
    def test_get(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)
        controller = ClientController()

        _, cid = controller.create(request)
        request = Request(RequestType.GetClient, cid, None, None)
        response = controller.get(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertEqual(response.data, data)

    def test_delete(self):
        data = DataClient(name='Boby', age=18).to_string()
        request = Request(RequestType.CreateClient, None, None, data)
        controller = ClientController()

        _, cid = controller.create(request)
        request = Request(RequestType.DeleteClient, cid, None, None)
        response = controller.delete(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertNotIn(cid, controller.data)


class TestTaskController(unittest.TestCase):
    def test_json_converter(self):
        data = DataTask(description="task of math").to_string()
        self.assertEqual(data, "{\"description\": \"task of math\"}")

    def test_new_client(self):
        controller = TasksController()
        cid = 1

        controller.new_client(cid)
        self.assertIn(cid, controller.data)
    
    def test_delete_client(self):
        controller = TasksController()
        cid = 1

        controller.new_client(cid)
        controller.delete_client(cid)
        self.assertNotIn(cid, controller.data)

    def test_create(self):
        controller = TasksController()
        controller.new_client(1)

        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, 1, "homework", data)
        response = controller.create(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(1, controller.data)
        self.assertIn("homework", controller.data[1])
        self.assertEqual(controller.data[1]["homework"].description, "task of math")

    def test_update(self):
        controller = TasksController()
        controller.new_client(1)

        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, 1, "homework", data)
        response = controller.create(request)

        data = DataTask(description="task of history").to_string()
        request = Request(RequestType.UpdateTask, 1, "homework", data)
        response = controller.update(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(1, controller.data)
        self.assertIn("homework", controller.data[1])
        self.assertEqual(controller.data[1]["homework"].description, "task of history")

    def test_delete(self):
        controller = TasksController()
        controller.new_client(1)

        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, 1, "homework", data)
        response = controller.create(request)

        request = Request(RequestType.DeleteTask, 1, "homework", None)
        response = controller.delete(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(1, controller.data)
        self.assertNotIn("homework", controller.data[1])

    def test_delete_all(self):
        controller = TasksController()
        controller.new_client(1)

        data = DataTask(description="task of math").to_string()
        request = Request(RequestType.CreateTask, 1, "homework1", data)
        response = controller.create(request)

        data = DataTask(description="task of histoy").to_string()
        request = Request(RequestType.CreateTask, 1, "homework2", data)
        response = controller.create(request)

        request = Request(RequestType.DeleteAllTasks, 1, None, None)
        response = controller.delete_all(request)

        self.assertTrue(response.status == ResponseType.Sucess, response.data)
        self.assertIn(1, controller.data)
        self.assertNotIn("homework1", controller.data[1])
        self.assertNotIn("homework2", controller.data[1])

if __name__ == '__main__':
    unittest.main()