import socket
import socket

def tcp_bind() -> socket.socket:
    try:
        port = int(input("Port to bind: "));
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(10)
        stream.bind(('localhost', port));
    except:
        return None
    return stream;

def tcp_connect() -> socket.socket:
    try:
        port = int(input("Port to connect: "));
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(10)
        stream.connect(('localhost', port));
    except:
        return None
    return stream;