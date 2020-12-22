#!/usr/bin/env python3

from sys import argv
from time import sleep, strftime, gmtime
from os import get_terminal_size, path, system
from file_manip import *


def try_import_me(lib_name:str, from_lib=''):
    try:
        exec_me = ""
        if from_lib != '':
            exec_me = f'from {lib_name} import {from_lib}'
        else:
            exec_me = f'import {lib_name}'
        exec(exec_me, globals())  # import the libs
    except ImportError:
        print(f'Install {lib_name} to run this program')
        def install_lib():
            permission = input('try to download it? [y/n]:').strip().lower()[0]
            if permission == 'y':
                system(f'pip3 install {lib_name}')  # install lib
                print('-' * 50)
        install_lib()

try_import_me('playsound', 'playsound')
try_import_me('notify2')


def get_argv() -> dict:
    conf = argv[1:]

    notification_mode = True
    if len(conf) >= 1:
        if '-n' in conf[0]:
            conf.pop(0)
            notification_mode = False
        if '-i' in conf[0]:
            return dict(notification_mode=notification_mode, Infinite=True)

    if len(conf) == 0:
        conf.append(25)
        conf.append(5)

    if len(conf) == 1:
        conf.append(5)

    not_int = []
    for x in conf:
        try:
            int(x)
        except Exception:
            not_int.append(x)

    x = ', '.join(not_int)
    if len(not_int) > 0:
        raise ValueError(f'Use int numbers! "{x}" != int')
    else:
        del(not_int)

    conf = (int(x) for x in conf)
    config = dict(zip(('work-time', 'short-break'), conf))

    config['notification_mode'] = notification_mode
    return config

    # Função para não ter que usar conf.append() toda hora
    # Talvez usar enum

def execute_times(config):
    try:
        notification_mode = config.get('notification_mode')
        config.pop('notification_mode')
    except Exception:
        pass

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        def time_counter():
            if notification_mode is True:
                notify2.init('python')
                n = notify2.Notification(f'{time}:00', f'{bt_title}')
                n.show()

            print(f'{"="*50}\n{bt_title.center(50)}\n{"="*50}')
            mytime = time*60
            for x in range(mytime):
                clock = strftime('%H:%M:%S', gmtime(mytime-1))
                beauty_print(clock)
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    keyboardinterrupt(dict(title=time))
                else:
                    mytime -= 1

        def beauty_print(clock):
            terminal_size = get_terminal_size(0)[0]
            if terminal_size >= 50:
                clock = ' '*int(25 - (len(clock)/2)) + clock
            print(f'\r{clock}', flush=True, end='')
        time_counter()
        print()

        try:
            playsound('sound.mp3')
        except Exception:
            try:
                playsound(path.expanduser('~/Pomodoro/sound.mp3'))
            except Exception:
                print('\nNO SOUND')
        print('\n')

    write(config)
    counter = read()

    if counter is False:
        counter = read()
    print(*counter, sep='\n')


def keyboardinterrupt():
    def save():
        with open('.pomodororc', 'r+') as configs:
            content = [x.replace('\n', '') for x in configs.readlines()]
            print(content)
            configs.write_through(content)
    save()
    while True:
        try:
            x = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            exit()
        else:
            try:
                x = (x.strip().lower())[0]
            except IndexError:
                exit()

        if x == 'y':
            print('Pomodoro will continue...')
            break
        elif x == 'n':
            exit()
        else:
            print('Invalid answer! Use Yes or No.')
            continue


if __name__ == '__main__':
    bad_variable_name = get_argv()
    while True:
        execute_times(bad_variable_name)
        keyboardinterrupt()

# Se o programa for fechado enquanto algum contador está rodando, salve-o
