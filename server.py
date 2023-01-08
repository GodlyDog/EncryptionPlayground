import socket
import threading
import encrypt
import time

HOST = "127.0.0.1"
PORT = 3000

listener = False
listener_conn = socket.socket()


def messaging(conn, keys):
    while True:
        send = input()
        encrypted = encrypt.encrypt(send, 'rsa', keys)
        conn.sendall(str(encrypted).encode('UTF-8'))
        if listener:
            listener_conn.sendall(str(encrypted).encode('UTF-8'))
        time.sleep(0.2)


def eavesdrop(conn):
    print("Someone is eavesdropping...")
    global listener
    listener = True
    global listener_conn
    listener_conn = conn
    message = "Happy eavesdropping!"
    listener_conn.sendall(message.encode('UTF-8'))
    while True:
        time.sleep(5)


def run_client(conn, addr):
    with conn:
        print("Connected to " + str(addr))
        connection_type = conn.recv(4096)
        connection_type = connection_type.decode('UTF-8')
        print(connection_type)
        if connection_type == "listener":
            eavesdrop(conn)
        else:
            server_keys = encrypt.keys('rsa')
            server_d = server_keys.pop()
            print(server_keys)
            encoded_keys = str(server_keys).encode('UTF-8')
            conn.sendall(encoded_keys)
            client_data = conn.recv(4096)
            client_keys = eval(client_data.decode('UTF-8'))
            print(client_keys)
            messaging_thread = threading.Thread(target=messaging, args=(conn, client_keys))
            messaging_thread.start()
            server_keys.append(server_d)
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                else:
                    if listener:
                        listener_conn.sendall(data)
                    decoded = eval(str(data, "UTF-8"))
                    message = encrypt.decrypt(decoded, 'rsa', tuple(server_keys))
                    message = "Received: " + message
                    print(message)


def listen(s):
    s.listen()
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=run_client, args=(connection, address))
        thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    listen(sock)
