#!/usr/bin/env python3

from contextlib import suppress
from time import sleep, strftime, gmtime
from sys import argv, platform
from os import get_terminal_size, path

# Dependencies
from plyer import notification
from playsound import playsound


def zl(a, b, fillvalue=None):  # My zip longest
    values = []

    for index, item in enumerate(a):
        try:
            values.append([item, b[index]])
        except Exception:
            fill = fillvalue[index]
            try:
                values.append([item, fill])
            except IndexError:
                values.append(item, fill[-1])
    return values


def get_argv():
    conf = [int(float(item.strip())) for item in argv[1:]]
    return conf[:3]


def times(conf):
    default = {'work': 25, 'rest': 5, 'long rest': 15}

    if conf == [] or conf == list(default.values()):
        return default

    return dict(zl(list(default), conf, fillvalue=list(default.values())))


class Notify():
    def __init__(self):
        self.title = ''
        self.time = 0

    def send_notification(self):
        self.playbell()
        notification.notify(  # Pop up notification
            title=f'{self.title.title()} is done!',
            message=f'{self.time}:00 minutes is about to run.',
            app_name='Pomodoro',
            timeout=10
        )

    def done(self):
        notification.notify(
            title='Pomodoro cicle is done!',
            message="Congratulations",
            app_name='Pomodoro',
            timeout=10
        )

    def playbell(self):
        if 'win' in platform:
            playsound(whereami()+'\\sounds\\sound.mp3')
        else:
            playsound(whereami()+'/sounds/sound.mp3')


def make_clock(time):
    return str(strftime('%M:%S', gmtime(int(time))))


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
            if keyboardinterrupt() == 'kill':
                break
            print(f'\n{banner(title)}')


def show_config(config):
    for x, y in config.items():
        print(f'{x.title()}: {make_clock(y*60)}', end=' ')
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
            return 'kill'
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


class Counter():
    def __init__(self):
        self.counter = 0

    def add(self):
        self.counter += 1

    def show(self):
        print(f'Counter: {self.counter}')

    def __str__(self):
        return f'Counter: {self.counter}'


def run_normal_config(config):
    notifi.time = config.get('rest')
    for title, time in config.items():
        print(banner(title))
        time_counter(title, time)
        print()

        notifi.title = title
        notifi.send_notification()
        notifi.time = time
        interval(title)


def run_long_config(config):
    notifi.time = config.get('long rest')
    for title, time in config.items():
        print(banner(title))
        time_counter(title, time)
        print()

        if title == 'long rest':
            notifi.done()
        else:
            notifi.title = title
            notifi.send_notification()
        interval(title)


if __name__ == '__main__':
    config = times(get_argv())
    notifi = Notify()
    counter = Counter()

    long_config = config_extractor(config)
    show_config(config)
    config.pop('long rest')

    for i in range(3):
        if i > 0:
            show_config(config)
        run_normal_config(config)
        counter.add()
        counter.show()
        print('-'*50)

    show_config(long_config)
    run_long_config(long_config)

    print('\nPomodoro is done!')
    print('-' * 50)

