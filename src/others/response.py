import json
from enum import IntEnum

class ResponseType(IntEnum):
    Sucess = 1
    Error = 2

class Response():
	def __init__(self, status: ResponseType, data):
		self.status = status.value
		self.data = data
        
	def to_string(self):
		return json.dumps(self.__dict__)
	
	staticmethod
	def from_string(data):
		obj = json.loads(data)
		status = ResponseType(int(obj['status']))
		return Response(status, obj['data'])  