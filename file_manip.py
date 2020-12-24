import json
from collections import Counter


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

