import socket
SERVER = "127.0.0.1"
PORT = 9090
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((SERVER, PORT))

while True:
    out_data = input("Введите сообщения для сервера: ")
    client_sock.sendall(out_data.encode())
    if out_data == 'exit':
        break

client_sock.close()