import sys
sys.path.append('.')

from others.inputs import USE_CID, USE_TASK, USE_BODY
from others.response import Response
from others.request import RequestType, make_request

def create(stream) -> Response:
	return make_request(stream, RequestType.CreateTask, USE_CID|USE_TASK|USE_BODY)

def update(stream)-> Response:
	return make_request(stream, RequestType.UpdateTask, USE_CID|USE_TASK|USE_BODY)

def list(stream) -> Response:
	return make_request(stream, RequestType.ListTasks, USE_CID)

def delete(stream) -> Response:
	return make_request(stream, RequestType.DeleteTask, USE_CID|USE_TASK)

def delete_all(stream) -> Response:
	return make_request(stream, RequestType.DeleteAllTasks, USE_CID)


