import binascii
import hashlib
import json
import os
from datetime import datetime
from hashlib import sha256
from flask import Flask, request, abort, jsonify, redirect, url_for

app = Flask(__name__)


def load():
    with open('auth.json', 'r', encoding='utf-8') as file:
        return list(json.load(file))


users = load()


def dump(auth):
    with open('auth.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(auth))


def check_login(login):
    global users
    return login in [user['login'] for user in users]


def check_existing(login):
    global users
    return True if login in [user['login'] for user in users] else False


def make_response(result=True, description=''):
    return {'result': result,
            'description': description}


def hash_password(password, salt: str = None):
    if salt:
        salt = salt.encode('ascii')
        new_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 80000)
        new_password = binascii.hexlify(new_password)
        return (salt + new_password).decode('ascii')
    else:
        salt = sha256(os.urandom(70)).hexdigest().encode('ascii')
        new_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 80000)
        new_password = binascii.hexlify(new_password)
        return (salt + new_password).decode('ascii'), salt.decode('ascii')


def registration_user(user):
    global users
    password, salt = hash_password(user['password'])
    new_user = {'login': user['login'],
               'password': password,
               'salt': salt,
               'date': datetime.now().isoformat()}
    users.append(new_user)
    dump(users)
    return make_response(True, 'Пользователь был зарегистрирован в системе'), 201


def check_password(user):
    global users
    login = user['login']
    password = user['password']
    try:
        checked_user = list(filter(lambda x: x['login'] == login, users))[0]
        checked_password = checked_user['password']
        checked_salt = checked_user['salt']
        new_password = hash_password(password, checked_salt)
        return checked_password == new_password
    except IndexError:
        return False


@app.route('/user/registration', methods=['POST'])
def registration_users():
    user = json.loads(request.get_data())
    if check_login(user['login']):
        return make_response(False, 'Данный пользователь уже зарегистрирован')
    else:
        return registration_user(user)


@app.route('/user/delete', methods=['DELETE'])
def delete_user():
    global users
    user = json.loads(request.get_data())
    if check_existing(user['login']):
        users = [user_info for user_info in users if user_info['login'] != user['login']]
        return make_response(True, 'Пользователь был удалён из системы'), 201
    else:
        return make_response(False, 'Данного пользователя не существует')


@app.route('/user/<string:username>', methods=['GET'])
def get_user(username):
    try:
        global users
        user = list(filter(lambda x: x['login'] == username, users))[0]
        print('print1 ', user)
        return jsonify({'users': user})
    except IndexError:
        abort(404)


@app.route('/users', methods=['GET'])
def get_users():
    global users
    return jsonify({'users': users})


@app.route('/auth', methods=['POST'])
def authorization_user():
    global users
    if check_login(json.loads(request.get_data())['login']) is True \
            and check_password(json.loads(request.get_data())['password']) is True:
        return make_response(True, 'Авторизация прошла успешно')
    elif check_login(json.loads(request.get_data())['login']) is True \
            and check_password(json.loads(request.get_data())) is False:
        return make_response(False, 'Некорректный пароль')
    elif check_login(json.loads(request.get_data())['login']) is False:
        return make_response(True, 'Некорректный логин')


@app.route('/')
def user_data():
    return 'Пользователи'


if __name__ == '__main__':
    app.run(host='127.0.0.1')

