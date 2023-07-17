#!/usr/bin/env python3

from time import sleep
from notify import Notify
from sysinfo import make_clock, return_terminal_size


def zl(a, b, fillvalue=None):  # My zip longest
    values = []
    for item_x, item_y in zip(a, b):
        values.append([item_x, item_y])

    remaining_items = a[len(b):]

    zl.counter = len(b)
    for remaining_item in remaining_items:
        values.append([remaining_item, fillvalue[zl.counter]])
        zl.counter += 1
    return values


def times(conf):
    default = {'work': 25, 'rest': 5, 'long rest': 15}

    if conf == [] or conf == list(default.values()):
        return default

    return dict(zl(list(default), conf, fillvalue=list(default.values())))


def banner(title):
    size = return_terminal_size()
    return f'{"="*size}\n{title.title().center(size)}\n{"="*size}'


def beauty_print(clock):
    clock = ' '*int((return_terminal_size()/2) - (len(clock)/2)) + clock
    print(f'\r{clock}\t', flush=True, end='')


def time_counter(title, time):
    for second in range((time*60), 0, -1):
        clock = make_clock(second)
        beauty_print(clock)

        try:
            sleep(1)
        except KeyboardInterrupt:
            if keyboardinterrupt():
                break
            print(f'\n{banner(title)}')


def show_config(config, toreturn=False):
    config_list = list()
    for x, y in config.items():
        config_list.append(f'{x.title()}: {make_clock(y*60)}')

    if toreturn:
        return ' | '.join(config_list)
    else:
        print(*config_list, sep=' ')
        print()


def keyboardinterrupt():
    while True:
        try:
            text = '\nDo you want to continue? [Y/n]\n>>> '
            resume_pomodoro = input(text).strip().lower()[0]
        except KeyboardInterrupt:
            exit()
        except IndexError:
            continue

        if resume_pomodoro == 'y':
            break
        elif resume_pomodoro == 'n':
            exit()
        elif resume_pomodoro == 'k':
            return True
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
    print("\n\n")


def config_extractor(config):
    long_config = config.copy()
    long_config.pop('rest')
    return long_config


def notification_check(notifi, title, time):
    if title == 'long rest':
        notifi.done()
    else:
        notifi.title = title
        notifi.send_notification()
        notifi.time = time


def run_configs(config):
    notifi = Notify(time=list(config.items())[-1][1])

    for title, time in config.items():
        print(banner(title))
        time_counter(title, time)
        print()

        notification_check(notifi, title, time)
        interval(title)
