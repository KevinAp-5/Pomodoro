import json
from collections import Counter
from time import strftime, gmtime


def creator():  # if raises FileNotFoundError: create the file
    config = dict(completed=0, worked=0, rested=0, total=0)
    try:
        with open('.pomodororc.json', 'w+') as pomodororc:
            json.dump(config, pomodororc, indent=4)
    except Exception:
        raise
    else:
        return config


def read():
    try:
        with open('.pomodororc.json', 'r+') as pomodororc:
            config = json.load(pomodororc)
    except (FileNotFoundError, IOError):
        return creator()
    except Exception:
        raise
    else:
        return config


def update_config(config):  # Update config values and return updated
    make_list = lambda _dict: [[x, y] for x, y in _dict.items()]
    old_config = make_list(convert_to(read(), int))  # Get the saved config

    config = make_list(config)
    for x in range(len(config)):
        if config[x][0] == 'work-time':
            config[x][0] = 'worked'
        if config[x][0] == 'rest-time':
            config[x][0] = 'rested'
    config = dict(config)

    for key, value in config.items():
        for index in range(len(old_config)):
            if old_config[index][0] == key:
                old_config[index][1] += value  # Updated value

    return dict(old_config)

def convert_to(config, convert_to=str): # Convert config to str or seconds
    if type(config) == dict:
        config = [[key, value] for key, value in config.items()]
    for x in range(len(config)):  # convert the minutes to seconds
        if config[x][0] in {'worked', 'rested'}:
            if convert_to == str:  # convert to hh:mm:ss
                if type(config[x][1]) != str:
                    config[x][1] = strftime('%H:%M:%S', gmtime(config[x][1]))

            elif convert_to == int:  # convert into seconds
                try:
                    h, m, s = config[x][1].split(':')
                except AttributeError:
                    pass
                else:
                    config[x][1] = int(h)*3600 + int(m)*60 + int(s)
    return dict(config)


def write(config:dict):
    config = convert_to(update_config(config))
    try:
        with open('.pomodororc.json', 'w+') as pomodororc:
            json.dump(config, pomodororc, indent=4)
    except Exception:
        raise

