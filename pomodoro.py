#!/usr/bin/env python3

from sys import argv
from os import system
from time import sleep, time
from playsound import playsound
from itertools import zip_longest

def get_argv():
    conf = argv
    conf.pop(0)  # Remove the python file name

    if len(conf) == 1: conf.append(5)
    if len(conf) == 0: return {'work-time':25, 'short-break':5}

    conf = (float(x) for x in conf)
    times = 'work-time', 'short-break', 'long-break'
    config = dict(zip_longest(times, conf, fillvalue=0))
    
    if 0 in config.values():
        config.pop(list(config.keys())[list(config.values()).index(0)])
        # Remove the key if the value is 0
    return config

def notification(config):
    for title, time in config.items():
        x = title.replace('-', ' ').capitalize()
        y = f'{time} minutes is counting.'
        system(f'notify-send "It is {x}!" "{y}"')  # Pop-up notification

        try:
            sleep(time*60)  # it's sleep... duh
        except KeyboardInterrupt:
            print("\nYour pomodoro clock isn't done.")
            exit()

        try:
            playsound('sound.mp3')
        except Exception:
            pass

        # Add images dos notification
        # Salvar quantas vezes o relogio pomodoro foi concluido.
        # Pause function

def pomodoro_count():
    """Conta as vezes que o pomodoro clock foi concluído."""
    pass

if __name__ == '__main__':
    notification(get_argv())

