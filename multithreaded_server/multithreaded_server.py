import socket
import threading


class ClientThread(threading.Thread):

    def __init__(self, client_address, client_conn):
        threading.Thread.__init__(self)
        self.client_socket = client_conn
        print("Добавлено новое соединение: ", client_address)

    def run(self):
        while True:
            data = self.client_socket.recv(2048)
            msg = data.decode()
            if msg:
                print(f"Сообщение от клиента {client_address}: ", msg)
            if msg == 'exit':
                print(f"Клиент из {client_address}, дисконектился...")
                break


LOCALHOST = "127.0.0.1"
PORT = 9090
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((LOCALHOST, PORT))
print("Старт сервера")
print("Ожидание клиента..")

while True:
    server_sock.listen(10)
    client_conn, client_address = server_sock.accept()
    newthread = ClientThread(client_address, client_conn)
    newthread.start()
