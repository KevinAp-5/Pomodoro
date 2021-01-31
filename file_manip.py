import json
from time import strftime, gmtime
from os.path import expanduser
from typing import Dict, List

json_path = expanduser('~/.pomodororc.json')


def creator() -> Dict:  # if raises FileNotFoundError: create the file
    config = dict(worked=0, rested=0, total=0)
    try:
        with open(json_path, 'w+') as pomodororc:
            json.dump(config, pomodororc, indent=4)
    except Exception:
        raise
    else:
        return config


def reset():
    """ Clean all the pomodororc content """
    try:
        with open(json_path, 'r+') as pomodororc:
            pomodororc.truncate(0)
    except Exception:
        raise
    else:
        creator()


def read() -> Dict:
    try:
        with open(json_path, 'r+') as pomodororc:
            try:
                config = json.load(pomodororc)
            except Exception:
                config = creator()
    except (FileNotFoundError, IOError):
        return creator()
    except Exception:
        raise
    else:
        return config


def update_config(config):  # Update config values and return updated
    def make_list(_dict: dict) -> list:
        return [[x, y] for x, y in _dict.items()]

    old_config = make_list(convert_to(read(), int))  # Get the saved config

    config = make_list(config)  # dict -> list

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

    old_config = dict(old_config)
    old_config['total'] = old_config['worked'] + old_config['rested']
    return old_config


def convert_to(config, convert_to=str):  # Convert config to str or seconds
    if type(config) == dict:
        config = [[key, value] for key, value in config.items()]
    for x in range(len(config)):  # convert the minutes to seconds
        if config[x][0] in {'worked', 'rested', 'total'}:
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


def write(config: dict):
    config = convert_to(update_config(config))
    try:
        with open(json_path, 'w+') as pomodororc:
            json.dump(config, pomodororc, indent=4)
    except Exception:
        raise

