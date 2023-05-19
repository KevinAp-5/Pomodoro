#!/usr/bin/env python3

from contextlib import suppress
from time import sleep, strftime, gmtime
from sys import argv, platform
from os import get_terminal_size, path

# Dependencies
from plyer import notification
from playsound import playsound


def get_greater(a, b):
    if len(b) > len(a):
        return b, a
    else:  # if 'a' is greater or equal to 'b'
        return a, b


def zl(a, b, fillvalue=None):  # My zip longest
    values = []
    for index in range(len(a)):  # zipping
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
    for index in range(len(conf)):
        if conf[index].isdigit():
            conf[index] = int(conf[index])
        else:  # float number in string format will return false in isdigit()
            with suppress(ValueError):
                conf[index] = int(float(conf[index]))
    return conf[:3]  # prevent random texts in argv


def times(conf):
    default = {'work': 25, 'rest': 5, 'long rest': 15}

    if conf == []:
        return default

    default_labels = list(default.keys()).copy()
    a, b = get_greater(default_labels, conf)
    return dict(zl(a, b, fillvalue=list(default.values())))


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


if __name__ == '__main__':
    config = times(get_argv())


    show_config(long_config)
    run_long_config(long_config)


    notifi = Notify()
    for sets in range(4):
        if sets == 3:
            config['rest'] = 15
        show_config(config)

        notifi.time = config.get('rest')
        for title, time in config.items():
            print(banner(title))
            notifi.title = title
            time_counter(title, time)
            print()

            if sets == 3 and 'rest' in title:
                notifi.done()
            else:
                notifi.send_notification()

            notifi.time = time
            interval(title)
            print()

        if sets == 3:
            print('Pomodoro is done!')
        else:
            print(f'Counter: {sets+1}')
        notifi.clear()

    print('-'*50)
