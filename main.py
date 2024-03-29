from pomodoro import times, config_extractor, show_config, run_configs, banner
from pomodoro import total_time, show_time, exec_time
from sysinfo import get_argv, terminal_size
from os import get_terminal_size
from time import sleep


def nice_line():
    line = '-' * int(terminal_size()*0.60)
    white_space = ' ' * int((terminal_size()/2) - (len(line)/2))
    line = f'{white_space}{line}{white_space}\n'
    sleep_time = 0.02

    for item in line:
        print(item, end='', flush=True)
        try:
            sleep(sleep_time)
        except KeyboardInterrupt:
            sleep_time = 0


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
    long_config = config_extractor(config)
    config.popitem()

    for counter, _ in enumerate(range(4), start=1):
        if counter == 4:
            config = long_config
            print(f'Stage {counter} - Final')
        else:
            print(f'Stage {counter}')

        show_config(config)
        run_configs(config)
        print_line()


@exec_time
def main():
    myconfig = config()
    pomodoro_stats = total_time(myconfig.copy())
    start(myconfig)
    run_clocks(myconfig)
    show_time(pomodoro_stats)


if __name__ == '__main__':
    main()
    print('\nPomodoro is done!')
