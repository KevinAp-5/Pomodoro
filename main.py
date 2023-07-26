from pomodoro import times, config_extractor, show_config, run_configs, banner
from sysinfo import get_argv
from os import get_terminal_size
from time import sleep


def terminal_size():
    return get_terminal_size()[0]


def nice_line():
    line = '-' * int(terminal_size()*0.60)
    white_space = ' ' * int((terminal_size()/2) - (len(line)/2))
    line = f'{white_space}{line}{white_space}\n'

    for item in line:
        print(item, end='', flush=True)
        try:
            sleep(0.02)
        except KeyboardInterrupt:
            pass


def start(config):
    print(banner('Pomodoro Clock'))
    print(f'{show_config(config, True)}'.center(terminal_size()))
    nice_line()


def print_line():
    size = int(terminal_size()*0.75)
    print('-'*size)


def config():
    return times(get_argv())


def run_clocks(config):
    config.pop('long rest')

    for i in range(3):
        print(f'Stage {i+1}')
        show_config(config)
        run_configs(config)
        print_line()

    print('Stage 4')
    long_config = config_extractor(config)
    show_config(long_config)
    run_configs(long_config)

    print('\nPomodoro is done!')
    print_line()


if __name__ == '__main__':
    myconfig = config()
    begin(myconfig)
    run_clocks(myconfig)
