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

def read():
    """Conta as vezes que o pomodoro clock foi concluído."""
    # Pegar o número atual salvo no arquivo, soma-lo a mais um e escrever
    # Tomar cuidado para n escrever a mesma coisa varias vezes no arquivo
    # Comi o cu de quem ta lendo

    # Le o arquivo e se não existir, ele cria
    try:
        with open('.pomodororc', 'r') as pomodororc:  # Tenta ler o arquívo
            counter = pomodororc.readlines()
    except FileNotFoundError:  # Se o arquívo não for encontrado, será criado
        print('File not found. The file will be created.')
        try:
            with open('.pomodororc', 'w+') as pomodororc:  # Just read it lol.
                pomodororc.write(f'completed times: 0')
        except Exception as error:
            print(f'occurred an error trying to create the file: {error}')
        else:
            print('the completed times counter is saved in .pomodororc')
    else:
        print('Printing pomodororc content:')

        if counter == []:
            print('The file is empty.')
            return False

        if len(counter) > 1:
            counter = counter[0]

        for x in counter:
            print(x)

def file_clean(filename):  # Just an easy way to delete all file content
    try:
        with open(filename, 'r+') as my_file:
            my_file.truncate(0)
    except:
        raise
    else:
        print('The file is clean.')

if __name__ == '__main__':
    read()

