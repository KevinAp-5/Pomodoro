#!/usr/bin/env python3

from sys import argv
from time import sleep, strftime, gmtime
from os import get_terminal_size, path, system
from file_manip import read, write, reset, show, where_ami
from playsound import playsound, PlaysoundException
from plyer import notification
from typing import Dict, Union
from itertools import repeat
from contextlib import suppress
from subprocess import run



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
    elif conf[0] == 'reset':
        reset()
        exit()
    elif conf[0] == 'show':
        show()
        exit()
    elif conf[0] in {'upgrade', 'update'}:
        check_upgrade()
        exit()
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
        a, b = get_greater(a, b)

        values = []
        counter = (x for x in range(len(a)))
        for x in range(len(a)):  # zipping
            index = next(counter)
            try:
                values.append([a[index], b[index]])
            except IndexError:
                fill = fillvalue[index]
                try:
                    values.append([a[index], fill])
                except IndexError:
                    values.append([a[index], fill[-1]])
        return values

    config = dict(
        zl(list(default.keys()), conf, fillvalue=list(default.values()))
    )
    return config


def execute_times(config):
    def clocked(time):
        """
        Retorna um relógio formatado baseado no tempo em segundos fornecido
        :param time: seconds
        :type time: int

        :return: retorna um relógio formatado
        :rtype: str
        """
        return str(strftime('%H:%M:%S', gmtime(int(time))))

    try:
        notification_mode = config.get('notification_mode')
        config.pop('notification_mode')
    except Exception:
        pass
    else:
        for x, y in config.items():
            print(f'{x.replace("-", " ")}: {clocked(y*60)}')

    def banner(title):  # return kind of a banner
        return f'{"="*50}\n{title.center(50)}\n{"="*50}'

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        def notify():
            if bt_title == 'rest time':
                level = 15  # critical
            else:
                level = 10  # normal

            notification.notify(  # Pop up notificatin
                title=f'{bt_title} is done!',
                message=f'Pomodoro Clock: {time}:00 was completed.',
                app_name='Pomodoro',
                timeout=level
            )

        def time_counter():
            if notification_mode is True:
                notify()
            else:
                print(banner(bt_title))

            mytime = time*60
            for x in range(mytime):
                x += 1
                clock = clocked(mytime-1)
                if notification_mode is False:
                    beauty_print(clock)
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    converted_to_second = {title: time * 60 - mytime}
                    keyboardinterrupt(converted_to_second, banner(bt_title))
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
            playsound(f'{where_ami()}/../sounds/sound.mp3')
        except PlaysoundException:
            pass
        finally:
            print()
            notify()  # replace this line with "pass" with you don't want
            # the notification's pop-up
        write({f'{title}': time*60})  # write the config numbers seconnds
    show() # print the time saved of pomodororc


def keyboardinterrupt(config=dict(), banner=None):  # called if user ctrl-c
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

    if banner:
        print('\n', banner, sep='')
    else:
        print()


if __name__ == '__main__':
    execute_times(get_argv())
