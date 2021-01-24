#!/usr/bin/env python3

from sys import argv
from time import sleep, strftime, gmtime
from os import get_terminal_size
from file_manip import read, write
from playsound import playsound
from plyer import notification
from typing import Dict, Union
from itertools import repeat
from contextlib import suppress


def get_argv() -> Dict[str, Union[bool, int]]:
    conf = [x.strip() for x in argv[1:]]  # Get argv stripped
    for x in range(len(conf)):  # will convert the strings to numbers
        if conf[x].isdigit():
            conf[x] = int(conf[x])
        else:  # float in a string returns false in isdigit()
            with suppress(ValueError):
                conf[x] = int(float(conf[x]))

    if len(conf) == 0:
        conf.insert(0, False)

    default = {'notification_mode': False, 'work-time': 25, 'rest-time': 5}

    if conf[0] == '-n':
        conf[0] = True
    elif type(conf[0]) == str:
        raise ValueError(f"Invalid command '{conf[0]}'")
    elif type(conf[0]) == int:
        conf.insert(0, False)

    def zl(a, b, fillvalue=None):
        def get_greater(a, b):
            if len(b) > len(a):
                return b, a  # return the greater
            else:  # if a is greater or is equal to b
                return a, b
        a, b = get_greater(a, b)  # len(a) > or == len(b)

        values = []
        counter = (x for x in range(len(a)))
        for x in range(len(a)):  # zipping
            c = next(counter)
            try:
                values.append([a[c], b[c]])
            except IndexError:
                fill = fillvalue[c]
                try:
                    values.append([a[c], fill])
                except IndexError:
                    values.append([a[c], fill[-1]])
        return values

    config = dict(
        zl(list(default.keys()), conf, fillvalue=list(default.values()))
    )
    return config


def execute_times(config):
    try:
        notification_mode = config.get('notification_mode')
        config.pop('notification_mode')
    except Exception:
        pass
    else:
        for x, y in config.items():
            print(f'{x.replace("-", " ")}: {y}')

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        def notify():
            if bt_title == 'rest time':
                level = 15  # critical
            else:
                level = 10  # normal

            notification.notify(  # Pop up notificatin
                title=f'{time}:00',
                message=bt_title,
                app_name='Pomodoro',
                timeout=level
            )

        def time_counter():
            if notification_mode is True:
                notify()
            else:
                print(f'{"="*50}\n{bt_title.center(50)}\n{"="*50}')

            mytime = time*60
            for x in range(mytime):
                clock = strftime('%H:%M:%S', gmtime(mytime))
                if notification_mode is False:
                    beauty_print(clock)
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    keyboardinterrupt({title: time*60 - mytime})
                else:
                    mytime -= 1

        def beauty_print(clock):
            try:
                terminal_size = get_terminal_size()[0]
            except OSError:  # it may rise if you're not running it on terminal
                terminal_size = 25

            if terminal_size >= 50:
                clock = ' '*int(25 - (len(clock)/2)) + clock
            print(f'\r{clock}\t', flush=True, end='')
        time_counter()
        print()

        try:
            playsound('sound.mp3')
        except Exception:
            notify()
            sleep(1.5)

    write(dict([[x, y*60] for x, y in config.items()]))  # convert the config
    # numbers into seconds to save it ex: 37:09

    for x, y in read().items():
        print(f'{x}: {y}')


def keyboardinterrupt(config=dict()):
    def write_exit():
        if config != dict():
            write(config)
        exit()
    while True:
        try:
            x = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            write_exit()
        else:
            try:
                x = (x.strip().lower())[0]
            except IndexError:
                exit()

        if x == 'y':
            print('Pomodoro will continue...')
            break
        elif x == 'n':
            write_exit()
        else:
            print('Invalid answer! Use Yes or No.')
            continue


if __name__ == '__main__':
    execute_times(get_argv())
