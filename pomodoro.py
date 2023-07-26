#!/usr/bin/env python3

from time import sleep
from notify import Notify
from sysinfo import make_clock, terminal_size
from keyboard import Keyboard


def zl(a, b, fillvalues=None):  # My zip longest
    values = []
    for item_a, item_b in zip(a, b):
        values.append([item_a, item_b])

    remaining_items = a[len(b):]

    for counter, remaining_item in enumerate(remaining_items, start=len(b)):
        values.append([remaining_item, fillvalues[counter]])
    return values


def times(config):
    default = {'work': 25, 'rest': 5, 'long rest': 15}

    if config == [] or config == list(default.values()):
        return default

    return dict(zl(list(default), config, fillvalues=list(default.values())))


def banner(title):
    size = terminal_size()
    return f'{"="*size}\n{title.title().center(size)}\n{"="*size}'


def beauty_print(clock):
    clock = ' '*int((terminal_size()/2) - (len(clock)/2)) + clock
    print(f'\r{clock}\t', flush=True, end='')


def show_config(config, returnable=False):
    config_list = list()
    for x, y in config.items():
        config_list.append(f'{x.title()}: {make_clock(y*60)}')

    if returnable:
        return ' | '.join(config_list)
    else:
        print(*config_list, sep=' ')
        print()


def keyboard_input(title):
    keyboard_signal = Keyboard().treat_input()

    if keyboard_signal:  # Should kill the clock
        return True
    print(f'\n{banner(title)}')


def time_counter(title, time):
    seconds = time * 60
    while seconds > 0:
        beauty_print(make_clock(seconds))
        try:
            sleep(1)
        except KeyboardInterrupt:
            if keyboard_input(title):
                break
            else:
                return True
        seconds -= 1


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
        while True:
            if not time_counter(title, time):
                break  # Kill the actual clock
            # restart the clock
        print()

        notification_check(notifi, title, time)
        interval(title)
