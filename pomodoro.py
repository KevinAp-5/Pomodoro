#!/usr/bin/env python3

from sys import argv
from time import sleep
from playsound import playsound
from os import get_terminal_size, path
import notify2


def get_argv():
    conf = argv[1:]

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

    conf = (int(x) for x in conf)
    times = 'work-time', 'short-break'
    config = dict(zip(times, conf))

    config['notification_mode'] = notification_mode
    return config


def execute_times(config):
    try:
        notification_mode = config.get('notification_mode')
        config.pop('notification_mode')
    except Exception:
        pass

    for title, time in config.items():
        bt_title = title.replace('-', ' ').title()

        if notification_mode is True:
            y = f'{time} minutes is counting.'
            notify2.init('python')
            n = notify2.Notification(f'notify-send "{bt_title}"', f'{y}')
            n.show()

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

            notify2.init('python')
            n = notify2.Notification(bt_title, f"{time} minutes is counting.")
            n.show()

            for x in range(time):  # Range of the minutes
                counter = 60
                for x in range(60):  # Range of the seconds
                    a, b = time-1, counter-1

                    if terminal_size >= 50:  # Will only print the beautiful
                        # print if the terminal size is > than 50
                        text = '{:02d}:{:02d}'.format(a, b)
                        x = ' ' * int((25 - (len(text)/2)))
                        text = x+text
                    else:
                        text = '{}: {:02d}:{:02d}'.format(bt_title, a, b)

                    print(f'\r{text}\t', flush=True, end='')  # Clock
                    try:
                        sleep(1)
                    except KeyboardInterrupt:
                        keyboardinterrupt()
                    except Exception:
                        raise

                    counter -= 1
                time -= 1
        try:
            playsound('sound.mp3')
        except Exception:
            try:
                playsound(path.expanduser('~/Pomodoro/sound.mp3'))
            except Exception:
                print('\nNO SOUND')
                print('mv or cp Pomodoro/sound.mp3 to /usr/local/bin')
        print('\n')

    write(config)
    counter = read()

    if counter is False:
        counter = read()
    print(*counter, sep='\n')


def keyboardinterrupt():
    while True:
        try:
            x = input('\nDo you want to continue? [Y/n]\n>>> ')
        except KeyboardInterrupt:
            exit()
        else:
            try:
                x = (x.strip().lower())[0]
            except IndexError:
                exit()

        if x == 'y':
            print('Pomodoro will continue...')
            break
        elif x == 'n':
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

        counter = (''.join(counter)).split('\n')
        try:
            counter.remove('')
        except Exception:
            pass
        return counter


def creater():
    write_me = ['completed: 0', 'worked: 00', 'rested: 00', 'total: 0']
    counter = 1
    for x in range(len(write_me)):
        write_me.insert(counter, '\n')
        counter += 2

    try:
        with open('.pomodororc', 'w+') as pomodororc:
            pomodororc.writelines(write_me)
    except Exception as error:
        print(f'occurred an error trying to create the file: {error}')


#  Class to threat the counter


def write(argv):
    try:
        counter = read()
    except Exception:
        raise
    else:
        if counter is False or counter is None:
            counter = read()

        for x in range(len(counter)):  # splits the strings
            counter[x] = [x.strip() for x in counter[x].split(':')]

        if 'total' not in counter[-1][0]:  # add the total if not found
            counter.append(['total', 0])

        counter = [[x[0], int(x[1])] for x in counter]

        a = 0
        for x in counter:
            if 'work' in x[0]:
                x[1] += argv.get('work-time')
                a += x[1]
            elif 'rest' in x[0]:
                x[1] += argv.get('short-break')
                a += x[1]
            elif 'completed' in x[0]:
                x[1] += 1
            elif 'total' in x[0]:
                x[1] = a

        for x in range(len(counter)):
            counter[x] = f'{counter[x][0]}: {counter[x][1]}'  # join strings

        count = 1
        for x in range(len(counter)):  # make a function to do it
            counter.insert(count, '\n')
            count += 2

        try:  # create the image
            with open('.pomodororc', 'w+') as pomodororc:
                pomodororc.writelines(counter)
        except Exception:
            raise


def file_clean():  # Just an easy way to delete all file content
    try:
        with open('.pomodororc', 'r+') as my_file:
            my_file.truncate(0)
    except Exception:
        raise
    else:
        print('The file is clean.')


if __name__ == '__main__':
    bad_variable_name = get_argv()
    while True:
        execute_times(bad_variable_name)
        keyboardinterrupt()

# Se o programa for fechado enquanto algum contador está rodando, salve-o
