import sys
sys.path.append('.')

from others.inputs import USE_CID, USE_BODY
from others.response import Response
from others.request import RequestType, make_request

def create(stream) -> Response:
	return make_request(stream, RequestType.CreateClient, USE_BODY)

def update(stream)-> Response:
	return make_request(stream, RequestType.UpdateClient, USE_CID|USE_BODY)

def get(stream) -> Response:
	return make_request(stream, RequestType.GetClient, USE_CID)

def delete(stream) -> Response:
	return make_request(stream, RequestType.DeleteClient, USE_CID)

