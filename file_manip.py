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


def update_config(config):
    old_config = [[key, value] for key, value in read().items()]

    index = (x for x in range(0, len(old_config), +1))
    for key, value in config.items():  # Update old_config to new values
        x = next(index)
        if key == old_config[x][0]:
            old_config[x][1] += value

    return dict(old_config)


# Salvar o tempo caso raise KeyboardInterrupt

