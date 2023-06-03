import socket
from settings import *


def authorization(sock):
    while True:
        response = sock.recv(2048).decode()
        print(response, end='')
        if CORRECT_PASSWORD in response:
            break
        print()
        request = input('>>>')
        sock.send(request.encode())


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    print(f'Присоединился к порту {PORT}')
    authorization(sock)
    with sock:
        while True:
            request = input()
            sock.send(request.encode())
            if request == 'exit':
                break
            response = sock.recv(1024).decode()
            print(response, end='')
            response = sock.recv(1024).decode()
            print(response, end='')


if __name__ == '__main__':
    main()