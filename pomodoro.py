from sys import argv
from os import system
from time import sleep, time
from playsound import playsound
from itertools import zip_longest

def get_argv():
    conf = argv
    conf.pop(0)  # Remove the python file name

    if len(conf) == 1: conf.append(5)
    if len(conf) == 0: return {'work-time':25.0, 'short-break':5.0}

    conf = (float(x) for x in conf)  # Int the conf items(argv)
    times = 'work-time', 'short-break', 'long-break'
    config = dict(zip_longest(times, conf, fillvalue=0))
    
    if 0 in config.values():
        try:
            config.pop(list(config.keys())[list(config.values()).index(0)])
            # Remove the key if the value is 0
        except Exception:
            pass
    return config

def notification(config):
    for title, time in config.items():
        x = title.replace('-', ' ')
        y = f'{time} minutes is counting'
        system(f'notify-send "{x}" "{y}"')  # Pop-up notification
        sleep(time*60)  # it's sleep... duh
        try:
            playsound('notification.mp3')
        except Exception:
            raise

def images():
    pass


if __name__ == '__main__':
    notification(get_argv())

