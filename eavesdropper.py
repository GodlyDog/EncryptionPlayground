import socket

HOST = "127.0.0.1"
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    connection_type = "listener"
    connection_type = connection_type.encode('UTF-8')
    sock.sendall(connection_type)
    while True:
        data = sock.recv(4096)
        if not data:
            break
        else:
            decoded = str(data, "UTF-8")
            message = "Received: " + decoded
            print(message)
