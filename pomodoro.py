#!/usr/bin/env python3

from time import sleep, time
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
    return dict(values)


def times(config):
    default = {'work': 25, 'rest': 5, 'long rest': 15}
    default_values = list(default.values())

    if config == [] or config == default_values:
        return default

    return zl(list(default), config, fillvalues=default_values)


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

    print(*config_list, sep=' ')
    print()


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
        notifi.send_notification(
            title='Pomodoro cicle is done!',
            message="Congratulations",
        )
    else:
        notifi.send_notification(
            title=f'{title.title()} is done!',
            message=f'{notifi.time}:00 minutes is about to run.',
        )
        notifi.time = time


def keyboard_input(title):
    keyboard_signal = Keyboard().treat_input()
    if keyboard_signal != 'kill':
        print(f'\n{banner(title)}')
    return keyboard_signal


def time_counter(title, time):
    seconds = time * 60
    while seconds > 0:
        beauty_print(make_clock(seconds-1))
        try:
            sleep(1)
        except KeyboardInterrupt:
            keyboard_out = keyboard_input(title)
            if keyboard_out == 'kill':
                return True
            elif keyboard_out is False:
                return False
            elif type(keyboard_out) == int:
                seconds = keyboard_out
            else:
                continue
        seconds -= 1
    return None


def run_configs(config):
    notifi = Notify(time=list(config.items())[-1][1])
    for title, clocks in config.items():
        print(banner(title))
        while True:
            should_kill = time_counter(title, clocks)
            if should_kill is True or should_kill is None:
                break
            else:
                continue
        print()

        notification_check(notifi, title, clocks)
        interval(title)


def total_time(config):
    long_rest = list(config_extractor(config).values())[::-1][0]

    config.popitem()
    config = list(config.items())

    total_time = {x: y*3 for x, y in config}
    total_time['rest'] += long_rest
    total_time.update({'Total time': sum(total_time.values())})
    return total_time


def show_time(total_time_output):
    for key, minutes in total_time_output.items():
        key = key+'ed' if key != 'Total time' else key

        format_time(key.title(), make_clock(minutes*60))


def format_time(title, clock):
    print('{:<12} {:^}{:>10}'.format(title, '->', clock))


def exec_time(func):
    def count_time():
        start = time()
        func()
        end = time()
        return format_time('Exec time', make_clock(int(end - start)))
    return count_time
