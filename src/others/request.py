import json
from enum import IntEnum
from time import sleep

from .inputs import get as get_inputs
from .response import Response, ResponseType

DATA_PAYLOAD = 4096

class RequestType(IntEnum):
	CreateTask = 1
	UpdateTask = 2 
	ListTasks = 3
	DeleteTask = 4
	DeleteAllTasks = 5

	CreateClient = 6
	UpdateClient = 7
	GetClient = 8
	DeleteClient = 9

class Request():
	def __init__(self, req: RequestType, cid, task, body):
		self.req = req.value
		self.cid = cid
		self.task = task
		self.body = body

	def to_string(self):
		return json.dumps(self.__dict__)
	
	staticmethod
	def from_string(data):
		obj = json.loads(data)
		req = RequestType(int(obj['req']))
		return Request(req, obj['cid'], obj['task'], obj['body'])  


def make_request(stream, req, mask):
	cid, task, body = get_inputs(mask)
	request = Request(req, cid, task, body)
	
	print(f'Sending request...')
	try:
		str_request = bytes(request.to_string(), 'utf-8')
		stream.send(str_request)
		while True:
			sleep(1)
			response = stream.recv(DATA_PAYLOAD)
			if response:
				break
		return Response.from_string(response.decode('utf-8'))
	except Exception as e: 
		return Response(ResponseType.Error, str(e))