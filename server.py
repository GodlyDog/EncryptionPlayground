import socket
import threading
import encryption

HOST = "127.0.0.1"
PORT = 3000


def run_client(conn, addr):
    with conn:
        print(f"Connected to {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


def listen(s):
    s.listen()
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=run_client, args=(connection, address))
        thread.start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    listen(sock)
