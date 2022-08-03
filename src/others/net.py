import socket

def tcp_bind() -> socket.socket:
    try:
        port = int(input("Port to bind: "))
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(30)
        stream.bind(('localhost', port))
        stream.listen(10)
    except:
        return None
    return stream;

def tcp_connect() -> socket.socket:
    try:
        port = int(input("Port to connect: "))
        stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream.settimeout(30)
        stream.connect(('localhost', port))
    except:
        return None
    return stream;