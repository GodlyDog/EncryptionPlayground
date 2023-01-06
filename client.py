import socket
import threading
import encrypt
import time

HOST = "127.0.0.1"
PORT = 3000


def messaging(s, keys):
    while True:
        send = input()
        encrypted = encrypt.encrypt(send, 'rsa', keys)
        s.sendall(str(encrypted).encode('UTF-8'))
        time.sleep(0.2)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    server_data = sock.recv(4096)
    server_keys = eval(server_data.decode('UTF-8'))
    print(server_keys)
    client_keys = encrypt.keys('rsa')
    client_d = client_keys.pop()
    print(client_keys)
    encoded_keys = str(client_keys).encode('UTF-8')
    sock.sendall(encoded_keys)
    messaging_thread = threading.Thread(target=messaging, args=(sock, server_keys))
    messaging_thread.start()
    client_keys.append(client_d)
    while True:
        data = sock.recv(4096)
        if not data:
            break
        else:
            decoded = eval(str(data, "UTF-8"))
            message = encrypt.decrypt(decoded, 'rsa', tuple(client_keys))
            message = "Received: " + message
            print(message)

