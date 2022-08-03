REPLICAS_PARAMETERS = {
    'repl1' : ('localhost:8001', ['localhost:8002', 'localhost:8003']),
    'repl2' : ('localhost:8002', ['localhost:8001', 'localhost:8003']),
    'repl3' : ('localhost:8003', ['localhost:8001', 'localhost:8002']),
    'tests' : ('localhost:8004', []),
}

REPLICAS_SOCKET_ADDRS = {
    'repl1' : ('localhost', 6001),
    'repl2' : ('localhost', 6002),
    'repl3' : ('localhost', 6003)
}