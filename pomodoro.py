#!/usr/bin/env python3

from sys import argv
from time import sleep, strftime, gmtime
from os import get_terminal_size
from file_manip import read, write
from playsound import playsound
from plyer import notification


def get_argv() -> dict:
    conf = argv[1:]  # Get argv without the python file name

    notification_mode = False
    if len(conf) >= 1:
        if '-n' in conf[0]:
            conf.pop(0)
            notification_mode = True

    if len(conf) == 0:
        conf.append(25)
        conf.append(5)

    if len(conf) == 1:
        conf.append(5)

    not_int = []
    for x in conf:
        try:
            int(x)
        except Exception:
            not_int.append(x)

    x = ', '.join(not_int)
    if len(not_int) > 0:
        raise ValueError(f'Use int numbers! "{x}" != int')
    else:
        del(not_int)

    config = dict(zip(('work-time', 'rest-time'), [int(x) for x in conf]))

    config['notification_mode'] = notification_mode
    return config

    # Função para não ter que usar conf.append() toda hora
    # Talvez usar enum


def execute_times(config):
    try:
        notification_mode = config.get('notification_mode')
        config.pop('notification_mode')
    except Exception:
        pass
    else:
        for x, y in config.items():
            x = x.replace('-', ' ')
            print(f'{x}: {y}')

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        def time_counter():
            if notification_mode is True:
                if bt_title == 'rest time':
                    level = 15  # critical
                else:
                    level = 10  # normal

                notification.notify(
                    title=f'{time}:00',
                    message=bt_title,
                    app_name='Pomodoro',
                    timeout=level

                )

            else:
                print(f'{"="*50}\n{bt_title.center(50)}\n{"="*50}')

            mytime = time*60
            for x in range(mytime):
                clock = strftime('%H:%M:%S', gmtime(mytime))
                if notification_mode is False:
                    beauty_print(clock)
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    keyboardinterrupt({title: time*60 - mytime})
                else:
                    mytime -= 1

        def beauty_print(clock):
            terminal_size = get_terminal_size()[0]
            if terminal_size >= 50:
                clock = ' '*int(25 - (len(clock)/2)) + clock
            print(f'\r{clock}\t', flush=True, end='')
        time_counter()
        print()

        try:
            playsound('sound.mp3')
        except Exception:
            pass
    write(dict([[x, y*60] for x, y in config.items()]))
    for x, y in read().items():
        print(f'{x}: {y}')


def keyboardinterrupt(config=dict()):
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


if __name__ == '__main__':
    execute_times(get_argv())
