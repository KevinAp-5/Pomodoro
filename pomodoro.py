#!/usr/bin/env python3

from sys import argv
from os import system, get_terminal_size
from time import sleep, time
from playsound import playsound
from itertools import zip_longest

def get_argv():
    conf = argv
    conf.pop(0)  # Remove the python file name

    terminal_mode = False
    if len(conf) >= 1:
        if '-t' in conf[0]:
            conf.pop(0)
            terminal_mode = True

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

    conf = (int(x) for x in conf)
    times = 'work-time', 'short-break', 'long-break'
    config = dict(zip_longest(times, conf, fillvalue=0))

    if 0 in config.values():
        config.pop(list(config.keys())[list(config.values()).index(0)])
        # Remove the key if the value of the key is 0

    config['terminal_mode'] = terminal_mode
    return config

def execute_times(config):
    terminal_mode = config.get('terminal_mode')
    config.pop('terminal_mode')

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        if terminal_mode is False:
            y = f'{time} minutes is counting.'
            system(f'notify-send "{bt_title}" "{y}"')

            try:
                sleep(time*60)  # "Convert" minutes into seconds
            except KeyboardInterrupt:
                keyboardinterrupt()
            except Exception:
                raise

        else:
            terminal_size = get_terminal_size(0)[0]
            if terminal_size >= 50:
                a = f'{bt_title}'.center(50)
                print(f'{"="*50}\n{a}\n{"="*50}')

            for x in range(time):  # Range of the minutes
                counter = 60
                for x in range(60):  # Range of the seconds
                    a, b = time-1, counter-1

                    if terminal_size >= 50:  # Just a beautiful print
                        text = '{:02d}:{:02d}'.format(a, b)
                        x = ' ' * int((25 - (len(text)/2)))
                        text = x+text
                    else:
                        text = '{:02d}:{:02d}'.format(a, b)

                    print(f'\r{text}\t', flush=True, end='')  # Clock
                    try:
                        sleep(1)
                    except KeyboardInterrupt:
                        keyboardinterrupt()
                    except Exception:
                        raise

                    counter -= 1
                time -= 1
        print('\n')
        # TODO add a song when time is done
        # TODO add the pomodoro counter

def keyboardinterrupt():
    while True:
        try:
            x = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            exit()
        else:
            x = (x.strip().lower())[0]

        if x == 'y':
            print('Pomodoro will continue...')
            break
        if x == 'n':
            a = input('Exiting, press [N] cancel.').strip().lower()
            if 'n' in a:
                continue
            else:
                print('Pomodoro is closing...')
                exit()
        else:
            print('Invalid answer! Use Yes or No.')
            continue

def read():
    try:
        with open('.pomodororc', 'r') as pomodororc:
            counter = pomodororc.readlines()
    except FileNotFoundError:
        creater()
    else:
        if counter == []:
            creater()
            return False

        counter = (''.join(counter)).split(':')
        counter[1] = (counter[1].replace('\n', '')).strip()
        return counter

def creater():
    try:
        with open('.pomodororc', 'w+') as pomodororc:
            pomodororc.write(f'completed times: 0\n')
    except Exception as error:
        print(f'occurred an error trying to create the file: {error}')
    else:
        print('the completed times counter is saved in .pomodororc')

def write():
    try:
        counter = read()
    except:
        raise
    else:
        if counter is False:
            counter = read()

        counter[1] = str(int(counter[1]) + 1)
        counter = ': '.join(counter)

        try:
            with open('.pomodororc', 'w+') as pomodororc:
                pomodororc.writelines(counter)
        except:
            raise
        else:
            print('Your config file is up to date.')

def file_clean(filename):  # Just an easy way to delete all file content
    try:
        with open(filename, 'r+') as my_file:
            my_file.truncate(0)
    except:
        raise
    else:
        print('The file is clean.')

#TODO adicionar o pomodoro em um terminal mode(sem ser notificação)
#usar o figlet para mostrar o tempo

if __name__ == '__main__':
    execute_times(get_argv())
