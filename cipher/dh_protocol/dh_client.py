import socket
import pickle

HOST = '127.0.0.1'
PORT = 9090

sock = socket.socket()
sock.connect((HOST, PORT))

g, p, a = 13, 8, 9
A = g ** a % p
sock.send(pickle.dumps((g, p, A)))

sock.close()