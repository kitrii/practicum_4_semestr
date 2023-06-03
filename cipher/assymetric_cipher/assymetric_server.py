import socket
import random

HOST = "127.0.0.1"
PORT = 65432


def generate_key_pair(g: int, p: int, A: int):
    b = random.randint(1, 5000)
    return (g ** b) % p, (A ** b) % p, b

def encode_message(key, message):
    return "".join([chr(int(str(key)[i%len(key)]) ^ ord(message[i])) for i in range(len(message))])

def decode_message(key, message):
    return "".join([chr(int(str(key)[i%len(key)]) ^ ord(message[i])) for i in range(len(message))])

def decrypt_message(b, p, g, message, B):
    K = (B ** b) % p
    return decode_message(str(K), message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Коннект сервера к хосту {addr}")
        msg = conn.recv(1024)
        data = msg.decode()
        g, p, A = data.strip().split(' ')
        print(f"Клиент получил данные -> g:{g}, p:{p}, A:{A}")
        pub_s, secret, b = generate_key_pair(int(g), int(p), int(A))
        print(f"Сгенерирована пара ключей -> Публичный: {pub_s}, Приватный: {secret}")
        conn.send(str(pub_s).encode())
        print(f"Публичный ключ отправлен!")
        msg = conn.recv(1024)
        data = msg.decode()
        message, B = data.split('SSS')
        print(f"Отправлено зашифрованное сообщение -> {message}")
        data = decrypt_message(int(b), int(p), int(g), message, int(B))
        print(f"Сообщение расшифровано -> {data}")
        conn.close()
