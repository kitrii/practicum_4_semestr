import os
import shutil


def help():
    commands = ['create',
                'delete',
                'rename',
                'read',  # только файл
                'whereami',
                'exit',
                'help',
                'copy',
                'move',
                'show',  # ls
                'change',  # изменяем файл
                'down',  # назад из папки
                'up',  # вперед в папку
                ]
    print(f'Доступны следующие команды:\n{commands}:')


def exception():
    print('Команда не распознана. Вам нужна помощь? [да/нет]')
    answer = input()
    if answer == 'да':
        help()
    else:
        print('Разбирайтесь сами!')


def create(name, a):
    if a == True:
        try:
            print(f'Создаю файл {name}')
            file = open(name, 'w+')
            file.close()
        except FileExistsError:
            print('Файл уже существует. Попробуйте изменить название.')
    elif a == False:
        try:
            print('Создаю папку')
            os.mkdir(os.path.normpath(os.getcwd() + '/' + name), mode=0o777)
        except FileExistsError:
            print('Файл уже существует. Попробуйте изменить название.')
    else:
        exception()


def delete(name, a):
    if not a:
        if os.path.isdir(name):
            shutil.rmtree(os.path.normpath(os.getcwd() + '/' + name), ignore_errors=False, onerror=None)
            print(f'Папка {name} удалена')
        else:
            print('Такой папки не существует.')
    elif a:
        if os.path.isfile(name):
            os.remove(name)
            print(f'Файл {name} удален')
        else:
            print('Такого файла не существует.')
    else:
        exception()


def rename(oldname):
    print('Введите новое имя:')
    newname = str(input())
    os.rename(oldname, newname)
    print('Переименовано')


def read(name, a):
    if a == True:
        file = open(name, 'r')
        print('Вывожу содержимое файла {}'.format(name))
        print(file.readlines())
        file.close()
    else:
        print('Такого файла нет. Возможно это папка')


def change(name, a):
    if a == True:
        file = open(name, 'w+')
        i = str(input('Введите текст, который нужно записать в файл: '))
        file.write(i)
        print("Текст записан")
        file.close()
    else:
        print('Такого файла нет. Возможно это папка')


def up(name, a):
    if a:
        print('Такой папки нет. Возможно это файл')
    elif not a:
        print(f'Перехожу в папку {a}.')
        os.chdir(os.getcwd() + '/' + name)
        print(f'Текущая папка {os.getcwd()}')


def copy(name):
    copy_name = str(input("Укажите название копии: "))
    i = str(input('Укажите абсолютный путь до папки, куда создать копию: '))
    try:
        fp = os.path.normpath(os.getcwd() + '/' + name)
        ds = os.path.normpath(i + '/' + copy_name)
        shutil.copy2(fp, ds)
    except FileNotFoundError and PermissionError:
        print('Для создания копии необходимо находится в папке оригинала.\nИ копировать можно только файлы.')


def move(name):
    path = str(input('Укажите абсолютный путь до папки, куда переместить:'))
    try:
        fp = os.path.normpath(os.getcwd() + '/' + name)
        ds = os.path.normpath(path)
        shutil.move(fp, ds)
        print(fp)
        print(ds)
    except (FileNotFoundError):
        print('Для перемещения необходимо находится в папке оригинала.')


def down(drr):
    a = os.getcwd()
    if a == drr:
        print('Вы находитесь в корневой папке.')
    else:
        print('Перехожу назад.')
        os.chdir('../..')
        print(f'Текущая папка {os.getcwd()}')

def main():
    with open('settings.txt', 'r') as settings:
        drr = os.path.normpath(settings.readline())
        print('Корневая директория', drr)
        settings.close()
    os.chdir(drr)

    while True:
        print('Введите команду: ')
        inp = input()
        try:
            act = str(inp).split(' ')
        except:
            act = str(inp)
        if len(act) > 1:
            if '.' in act[1]:
                a = True
            else:
                a = False

        if act[0] == 'create':
            create(str(act[1]), a)

        elif act[0] == 'delete':
            delete(str(act[1]), a)

        elif act[0] == 'rename':
            rename(str(act[1]))

        elif act[0] == 'read':
            read(str(act[1]), a)

        elif act[0] == 'whereami':
            print(os.getcwd())

        elif act[0] == 'help':
            help()

        elif act[0] == 'copy':
            copy(str(act[1]))

        elif act[0] == 'exit':
            print('Всего доброго!')
            break

        elif act[0] == 'show':
            print(os.listdir())

        elif act[0] == 'move':
            move(str(act[1]))

        elif act[0] == 'change':
            change(str(act[1]), a)

        elif act[0] == 'up':
            try:
                up(act[1], a)
            except IndexError:
                print('Название папки отсутствует')
            except FileNotFoundError:
                print('Папка не существует')

        elif act[0] == 'down':
            down(drr)
        else:
            exception()


main()
