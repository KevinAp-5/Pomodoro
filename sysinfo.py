from sys import platform, argv
from os import path, get_terminal_size
from time import strftime, gmtime
from contextlib import suppress


def make_clock(time):
    time_format = ''

    if time >= 60*60:
        time_format = '%H:%M:%S'
    else:
        time_format = '%M:%S'

    return str(strftime(time_format, gmtime(int(time))))


def terminal_size():
    terminalSize = get_terminal_size()[0]
    if (terminalSize > 100):
        return 100
    return terminalSize
    


def get_argv():
    conf = [int(float(item.strip())) for item in argv[1:]]
    return conf[:3]
