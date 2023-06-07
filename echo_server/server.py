import json
import random
import socket
import logging

logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.INFO)


def log(message):
    logging.info(message)
    print(message)


log('Запуск сервера')
sock = socket.socket()
port = int(input("Введите номер порта, к которому хотите подключиться: "))
try:
    sock.bind(('', port))
    log(f"Начало прослушивания порта {port}")
except:
    random_port = random.randint(9000, 10000)
    sock.bind(('', random_port))
    log(f"Не получилось подключиться к порту {port}! Начало прослушивания порта {random_port}!")

sock.listen(1)
conn, address = sock.accept()


with open('auth.json', 'r') as auth:
    file = json.loads(auth.read())
    if address[0] == file['host']:
        log(f"Welcome! {file['name']}".encode())
    else:
        with open('auth.json', 'w') as auth:
            auth.write(json.dumps({"host": f"{address[0]}", "name": "Stranger"}))

while True:
    log("Подключился клиент")

    data = conn.recv(1024).decode()

    if data:
        if data == 'exit':
            log('Клиент отключился')
            conn, address = sock.accept()
        log("Прием данных от клиента")
        log(data)
        conn.send(str(data).encode())
        log("Отправка данных клиенту обратно")


