import os

HOST = '127.0.0.1'
PORT = 9085

REQUEST_LOGIN = 'Введите логин:'
REQUEST_PASSWORD = 'Введите пароль:'
REQUEST_NEW_PASSWORD = 'Введите новый пароль:'
INCORRECT_PASSWORD = 'Неверный пароль'
CORRECT_PASSWORD = 'Вход выполнен'

INCORRECT_PATH = 'Такой путь не существует'
LACK_OF_MEMORY = 'Недостаточно места на диске'
ENCODING = 'UTF-8'
BUFFER_SIZE = 1024
AUTH_FILE = 'credential_auth.json'
SEP = os.sep
WORKING_DIRECTORY = os.getcwd() + SEP + 'documents'
ADMIN = 'admin'
MAX_DIRECTORY_SIZE = 50
LOG = WORKING_DIRECTORY + SEP + 'log.txt'
