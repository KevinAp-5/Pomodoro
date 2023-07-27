from sys import platform, argv
from os import path, get_terminal_size
from time import strftime, gmtime
from contextlib import suppress


def whereami(index=1) -> str:
    """Return the path of where the python script is running at"""
    with suppress():
        if 'win' in platform:
            return "\\".join(path.realpath(__file__).split('\\')[:-index])
        else:
            return '/'.join(path.realpath(__file__).split('/')[:-index])


def make_clock(time, time_format=None):
    if time_format:
        time_format = '%H:%M:%S'
    else:
        time_format = '%M:%S'

    return str(strftime(time_format, gmtime(int(time))))


def terminal_size():
    try:
        terminal_size = get_terminal_size()[0]
    except OSError:  # it may rise if you're not running it on terminal
        terminal_size = 30
    return terminal_size


def get_argv():
    conf = [int(float(item.strip())) for item in argv[1:]]
    return conf[:3]
