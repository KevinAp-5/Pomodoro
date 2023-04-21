#!/usr/bin/env python3

from contextlib import suppress
from time import sleep, strftime, gmtime
from sys import argv, platform
from os import get_terminal_size, path, system

# Dependencies
from plyer import notification
from playsound import playsound, PlaysoundException

def get_greater(a, b):
    if len(b) > len(a):
        return b, a
    else:  # if 'a' is greater or equal to 'b'
        return a, b

def zl(a, b, fillvalue=None):  # My zip longest
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

def get_argv():
    conf = [x.strip() for x in argv[1:]]  # Get argv stripped

    # will convert the strings to numbers
    for x in range(len(conf)):
        if conf[x].isdigit():
            conf[x] = int(conf[x])
        else:  # float number in string format will return false in isdigit()
            with suppress(ValueError):
                conf[x] = int(float(conf[x]))
    return conf[:2]  # prevent random texts in argv

def times(conf):
    default = {'work': 25, 'rest': 5}
    default_labels = list(default.keys()).copy()

    return dict(zl(default_labels, conf, fillvalue=list(default.values())))

# --------------------
def make_clock(time):
    return str(strftime('%M:%S', gmtime(int(time))))

def notify(title, time):
    notification.notify(  # Pop up notification
        title=f'{title.title()} is done!',
        message=f'{time}:00 was completed.',
        app_name='Pomodoro',
        timeout=10)

def whereami(index=1) -> str:
    """Return the path of where the python script is running at"""
    with suppress():
        if 'win' in platform:
            return "\\".join(path.realpath(__file__).split('\\')[:-index])
        else:
            return '/'.join(path.realpath(__file__).split('/')[:-index])

def return_terminal_size():
    try:
        terminal_size = get_terminal_size()[0]
    except OSError:  # it may rise if you're not running it on terminal
        terminal_size = 30
    return terminal_size

def banner(title):  # return a banner
    size = return_terminal_size()
    return f'{"="*size}\n{title.title().center(size)}\n{"="*size}'

def beauty_print(clock):
    clock = ' '*int((return_terminal_size()/2) - (len(clock)/2)) + clock
    print(f'\r{clock}\t', flush=True, end='')

def time_counter(title, time):
    seconds = (time*60) + 1
    for second in range(seconds):
        clock = make_clock(seconds-1)
        beauty_print(clock)

        try:
            sleep(1)
        except KeyboardInterrupt:
            keyboardinterrupt()
            print('\n', banner(title), sep='')
        else:
            seconds -= 1

def show_config(config):
    for x, y in config.items():
        print(f'{x.title()}: {make_clock(y*60)}', end=' ')
    print()

def playbell():
    if 'win' in platform:
        playsound(whereami()+'\\sounds\\sound.mp3')
    else:
        playsound(whereami()+'/sounds/sound.mp3')

def keyboardinterrupt():
    while True:
        try:
            resume_pomodoro = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            exit()
        else:
            try:
                resume_pomodoro = (resume_pomodoro.strip().lower())[0]
            except IndexError:
                continue

        if resume_pomodoro == 'y':
            break
        elif resume_pomodoro == 'n':
            exit()
        else:
            print('Invalid answer! Use Yes or No.')
            continue

def interval(title):
    print(f'{title} is done!', end=' ')
    for letter in '.'*10:
        print(letter, end='', flush=True)
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
    print()

def run_part(title, time):
    print(banner(title))
    time_counter(title, time)
    print()
    playbell()
    notify(title, time)
    interval(title)

def cycle_count(config):
    for sets in range(4):
        if sets == 3:
            config['rest'] = 15
        for title, time in config.items():
            run_part(title, time)
        print(f'{sets+1} sets already done')
        show_config(config)
    print('-'*50)

if __name__ == '__main__':
    config = times(get_argv())
    show_config(config)
    cycle_count(config)

