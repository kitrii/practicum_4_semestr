import os
import shutil


def help():
    commands = ['создать', 'удалить', 'назад', 'переименовать', 'выход', 'показать', 'справка',
                'где', 'показать', 'вперед', 'читать', 'редактировать',  'копировать', 'переход']
    print(f'Доступны следующие команды:\n{commands}:')


def exception():
    print('Команда не распознана. Хотите вызвать помощника? [да/нет]')
    yn = input()
    if yn == 'да':
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
            print('Создаю папку...')
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
    print('Переименовано.')


def read(name, a):
    if a == True:
        file = open(name, 'r')
        print('Вывожу содержимое файла {}'.format(name))
        print(file.readlines())
        file.close()
    else:
        print('Кажется это папка, а не файл.')


def change(name, a):
    if a == True:
        file = open(name, 'w+')
        i = str(input('Введите текст, который нужно записать в файл: '))
        file.write(i)
        print("Текст записан")
        file.close()
    else:
        print('Кажется это папка, а не файл.')


def up(name, a):
    if a:
        print('Кажется это файл, а не папка.')
    elif not a:
        print('Перехожу в папку {}...'.format(name))
        os.chdir(os.getcwd() + '/' + name)
        print(f'Текущая папка {os.getcwd()}')


def copy(name, drr):
    copy_name = str(input("Укажите название копии: "))
    i = str(input('Укажите абсолютный путь до папки, куда создать копию: '))
    try:
        fp = os.path.normpath(os.getcwd() + '/' + name)
        ds = os.path.normpath(i + '/' + copy_name)
        shutil.copy2(fp, ds)
    except FileNotFoundError and PermissionError:
        print('Для создания копии необходимо находится в папке оригинала.\nИ копировать можно только файлы.')


def move(name, drr):
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
        print('Перехожу назад...')
        os.chdir('../..')
        print(f'Текущая папка {os.getcwd()}')

def main():
    with open('settings.txt', 'r') as settings:
        drr = os.path.normpath(settings.readline())
        print('Корневая директория', drr)
        settings.close()
    os.chdir(drr)

    while True:
        print('Введите команду:')
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

        if act[0] == 'выход':
            print('Всего доброго!')
            break

        elif act[0] == 'справка':
            help()

        elif act[0] == 'создать':
            create(str(act[1]), a)

        elif act[0] == 'удалить':
            delete(str(act[1]), a)

        elif act[0] == 'переименовать':
            rename(str(act[1]))

        elif act[0] == 'где':
            print(os.getcwd())

        elif act[0] == 'показать':
            print(os.listdir())

        elif act[0] == 'вперед':
            try:
                up(act[1], a)
            except IndexError:
                print('Название папки отсутствует')
            except FileNotFoundError:
                print('Папка не существует')

        elif act[0] == 'назад':
            down(drr)

        elif act[0] == 'редактировать':
            change(str(act[1]), a)

        elif act[0] == 'читать':
            read(str(act[1]), a)

        elif act[0] == 'копировать':
            copy(str(act[1]), drr)

        elif act[0] == 'переместить':
            move(str(act[1]), drr)

        else:
            exception()


main()
