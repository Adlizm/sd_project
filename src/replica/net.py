import socket

from .config import REPLICAS_SOCKET_ADDRS

def connect_replica(replica_name):
    if not replica_name in REPLICAS_SOCKET_ADDRS:
        return None
    host, port = REPLICAS_SOCKET_ADDRS[replica_name]

    try:
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(30)
        stream.connect((host, port))
        return stream;  
    except:
        return None

def bind_replica(replica_name):
    if not replica_name in REPLICAS_SOCKET_ADDRS:
        return None
    host, port = REPLICAS_SOCKET_ADDRS[replica_name]

    try:
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(30)
        stream.bind((host, port))
        stream.listen(10)
        return stream;  
    except:
        return None