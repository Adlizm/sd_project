import etcd3

ENDPOITS = [
    etcd3.Endpoint(host='localhost', port=12379, secure=False),
    etcd3.Endpoint(host='localhost', port=22379, secure=False),
    etcd3.Endpoint(host='localhost', port=32379, secure=False),
]

def create_client_etcd():
    return etcd3.MultiEndpointEtcd3Client(endpoints=ENDPOITS)
