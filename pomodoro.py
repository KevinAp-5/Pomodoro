#!/usr/bin/env python3

from plyer import notification
from typing import Dict
from sys import argv, platform
from contextlib import suppress
from os import get_terminal_size, path
from time import sleep, strftime, gmtime
from playsound import playsound, PlaysoundException

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

def get_argv() -> Dict[str, int]:
    conf = [x.strip() for x in argv[1:]]  # Get argv stripped
    for x in range(len(conf)):  # will convert the strings to numbers
        if conf[x].isdigit():
            conf[x] = int(conf[x])
        else:  # float in a string returns false in isdigit()
            with suppress(ValueError):
                conf[x] = int(float(conf[x]))
    conf = conf[:2]  # To prevent a lot of random texts in argv

    default = {'work': 25, 'rest': 5}

    default_labels = list(default.keys()).copy()

    return dict(zl(default_labels, conf, fillvalue=list(default.values())))

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

def whereami(index=1) -> str:
    """Return the path of where the python script is running in"""
    with suppress():
        if platform == 'win32':
            return "\\".join(path.realpath(__file__).split('\\')[:-index])
        else:
            return '/'.join(path.realpath(__file__).split('/')[:-index])

def beauty_print(clock):
    try:
        terminal_size = get_terminal_size()[0]
    except OSError:  # it may rise if you're not running it on terminal
        terminal_size = 25

    if terminal_size >= 50:
        clock = ' '*int(25 - (len(clock)/2)) + clock
    print(f'\r{clock}\t', flush=True, end='')

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

        time_counter()
        print()

        try:
            if platform == 'win32':
                playsound(whereami()+'\\sounds\\sound.mp3')
            else:
                playsound(whereami()+'/sounds/sound.mp3')
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

