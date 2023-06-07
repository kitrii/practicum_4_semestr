import socket

host_name = input('Введите имя хоста (127.0.0.1 по-умолчанию): ')

sock = socket.socket()
port = int(input("Введите номер порта, к которому хотите подключиться: "))

if host_name:
    sock.connect((host_name, port))
else:
    sock.connect(('', port))


print("Соединение с сервером")

while True:
    word = input("Введите сообщение для сервера: ")
    sock.send(word.encode())
    print('Отправка данных серверу')
    data = sock.recv(1024).decode()
    print(f"Получение сообщения от сервера обратно {data}")
    if word == 'exit':
        print('Разрыв соединения с сервером')
        sock.close()
        break
