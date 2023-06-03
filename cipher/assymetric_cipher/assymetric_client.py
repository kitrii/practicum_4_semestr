import socket
import random

HOST = "127.0.0.1"
PORT = 65432


def generate_key_pair_client(init: bool = True, a: int = None, g:int = None, p: int = None, B: int = None):
    if init:
        if p == None:
            p = 999 # хардкодный p
        if g == None:
            g = random.randint(22, 5000)
        if a == None:
            a = random.randint(22, 5000)

        return (g ** a) % p, g, p, a
    else:
        return (B ** a) % p


def encode_message(key, message):
    return "".join([chr(int(str(key)[i % len(key)]) ^ ord(message[i])) for i in range(len(message))])


def decode_message(key, message):
    return "".join([chr(int(str(key)[i % len(key)]) ^ ord(message[i])) for i in range(len(message))])


def form_encrypted_message(p, g, A, message):
    b = random.randint(22, 5000)
    K = (A ** b) % p
    B = (g ** b) % p

    return encode_message(str(K), message), B


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Коннект к хосту: {HOST}")
    pub_c, g, p, a = generate_key_pair_client(init=True)
    print(f"Числа сгенерированы: g:{g}, p:{p}, A:{pub_c}")
    data = f"{g} {p} {pub_c}"
    s.send(data.encode())
    msg = s.recv(1024)
    data = msg.decode()
    pub_s = data.strip()
    print(f"Получен публичный ключ сервера: {pub_s}")
    secret_c = generate_key_pair_client(init=False, B=int(pub_s), a=a, p=p)
    print(f"Общий ключ: {secret_c}")
    to_enc = "Клиент передает привет!"
    message, B = form_encrypted_message(int(p), int(g), int(pub_s), to_enc)
    data = "SSS".join([message, str(B)])
    s.send(data.encode())
    print(f"Отправлено зашифрованное сообщение:\n Сообщение: {to_enc}, Зашифр.сообщение: {data}")
    s.close()