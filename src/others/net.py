import socket
import random

def portal_client_addrs(): 
    return [ ('localhost', 4000), ('localhost', 4001) ]

def portal_admin_addrs():
    return [ ('localhost', 5000), ('localhost', 5001) ]

def bind_one(addrs) -> socket.socket:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    bind = False
    for addr in addrs:
        try:
            tcp.bind(addr)
        except:
            continue
        finally:
            bind = True
    if not bind:
        return None
    
    tcp.listen(10)
    return tcp

def connect_one(addrs: list) -> socket.socket:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(10)
    
    connected = False
    for _ in range(len(addrs)):
        try:
            addr = random.choice(addrs)
            tcp.connect(addr)
        except:
            addrs.remove(addr)
            continue
        finally:
            connected = True
    if not connected:
        return None

    return tcp