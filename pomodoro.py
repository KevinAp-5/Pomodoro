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
    conf = [x.strip() for x in argv[1:]]  # Get argv stripped

    if conf == []:
        return conf
    else:
        conf = [int(float(item)) for item in conf]
        return conf[:3]


def times(conf):
    default = {'work': 25, 'rest': 5, 'long rest': 15}

    if conf == [] or conf == list(default.values()):
        return default

    return dict(zl(list(default), conf, fillvalue=list(default.values())))


class Notify():
    def __init__(self, title='', time=0):
        self.title = title
        self.time = time

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
            if keyboardinterrupt() == 'kill':
                break
            print('\n', banner(title), sep='')
        else:
            seconds -= 1


def show_config(config):
    for x, y in config.items():
        print(f'{x.title()}: {make_clock(y*60)}', end=' ')
    print()


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
    long_config = {
        'work': config.get('work'),
        'long rest': config.get('long rest')
    }
    return long_config


class Counter():
    def __init__(self):
        self.counter = 0

    def add(self):
        self.counter += 1

    def show(self):
        print(f'Counter: {self.counter}')

    def __repr__(self):
        return self.counter

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

