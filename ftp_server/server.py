import json
import socket
from datetime import datetime

from file_manager import *
from settings import *


def read_creds(file=AUTH_FILE):
    with open(file, 'r', encoding=ENCODING) as creds:
        logins = json.load(creds)
    return logins


def write_auth(fileName, data, currentPath=os.getcwd()):
    os.chdir(WORKING_DIRECTORY)
    data.update(read_creds(fileName))
    json.dump(data, open(fileName, 'w', encoding=ENCODING), sort_keys=True)
    os.chdir(currentPath)


def writeLog(fileName, text):
    with open(fileName, 'a', encoding=ENCODING) as logFile:
        logFile.write(f"{'-' * 25}\n{datetime.now()}: {text}\n")


def req_password(sock, conn, correctPassword, login):
    password = make_request(conn, REQUEST_PASSWORD)
    if password == correctPassword:
        handle(sock, conn, login)
    else:
        req_password(sock, conn, correctPassword, login)


def requestNewPassword(sock, conn, login):
    newPassword = make_request(conn, REQUEST_NEW_PASSWORD)
    write_auth(AUTH_FILE, {login: newPassword}, currentPath=os.getcwd())
    handle(sock, conn, login)


def make_request(conn, message):
    send(conn, message)
    return recv(conn)


def send(conn, message, encoding=ENCODING):
    conn.send(message.encode(encoding))


def recv(conn: socket.socket, bufSize=BUFFER_SIZE, encoding=ENCODING):
    return conn.recv(bufSize).decode(encoding)


def authorization(sock, conn):
    logins = read_creds()
    login = make_request(conn, REQUEST_LOGIN)
    if login in logins:
        req_password(sock, conn, logins[login], login)
    else:
        requestNewPassword(sock, conn, login)


def accept(sock):
    while True:
        try:
            conn = sock.accept()[0]
            authorization(sock, conn)
        except:
            raise AssertionError


def main():
    os.chdir(WORKING_DIRECTORY)
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)
    print(f'Прослушивание порта {PORT}')
    accept(sock)


if __name__ == '__main__':
    main()