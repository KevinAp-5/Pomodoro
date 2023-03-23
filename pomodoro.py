#!/usr/bin/env python3

from sys import argv, platform
from time import sleep, strftime, gmtime
from os import get_terminal_size
from file_manip import write, reset, show, whereami
from playsound import playsound, PlaysoundException
from plyer import notification
from typing import Dict, Union
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

    default = {'work': 25, 'rest': 5}

    if conf[0] == 'show':
        show()
    elif type(conf[0]) == str:
        raise ValueError(f"Invalid command '{conf[0]}'")
    elif type(conf[0]) == int:
        conf.insert(0, False)

    conf = conf[:5]  # To prevent a lot of random texts in argv

    strings = list()
    for x in conf[1:]:
        if type(x) == str:
            strings.append(x)

    if len(strings) != 0:
        strings = strings[:2]

    for x in strings:
        if x in conf:
            conf.remove(x)

    def zl(a, b, fillvalue=None):  # My zip longest
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

    label_keys = list()
    if strings:
        strings.insert(0, list(default.keys())[0])
        label_keys = strings.copy()
        del strings
    else:
        label_keys = list(default.keys()).copy()

    if len(label_keys) < len(conf):
        label_keys.append(list(default.keys())[-1])

    config = dict(
        zl(label_keys, conf, fillvalue=list(default.values()))
    )
    return config

# --------------------
def make_clock(time):
    """
    Retorna um relógio formatado baseado no tempo em segundos fornecido
    :param time: seconds
    :type time: int

    :return: retorna um relógio formatado
    """
    return str(strftime('%H:%M:%S', gmtime(int(time))))

def banner(title):  # return kind of a banner
    return f'{"="*50}\n{title.center(50)}\n{"="*50}'

def notify(bt_title, time, timeout_time=10):
    if bt_title == 'rest time':
        timeout_time = 15  # critical

    notification.notify(  # Pop up notification
        title=f'{bt_title} is done!',
        message=f'Pomodoro Clock: {time}:00 was completed.',
        app_name='Pomodoro',
        timeout=timeout_time
    )

def execute_times(config):
    for x, y in config.items():
        print(f'{x}: {make_clock(y*60)}')

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        def time_counter():
            print(banner(bt_title))

            mytime = time*60
            for x in range(mytime):
                x += 1
                clock = make_clock(mytime-1)
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
            if platform == 'win32':
                playsound(whereami(1)+'\\sounds\\sound.mp3')
            else:
                playsound(whereami(1)+'/sounds/sound.mp3')
        except PlaysoundException:
            print()
            notify(bt_title, time, timeout_time=15)
        else:
            print()
            notify(bt_title, time)  # replace with 'pass' to no notification

def keyboardinterrupt(config=dict(), banner=None):  # called if user ctrl-c
    while True:
        try:
            exiting = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            exit()
        else:
            try:
                exiting = (exiting.strip().lower())[0]
            except IndexError:
                exit()

        if exiting == 'y':
            print('Pomodoro will continue...')
            break
        elif exiting == 'n':
            exit()
        else:
            print('Invalid answer! Use Yes or No.')
            continue

    if banner:
        print('\n', banner, sep='')
    else:
        print()


if __name__ == '__main__':
    execute_times(get_argv())
