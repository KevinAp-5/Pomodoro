from pomodoro import times, config_extractor, show_config, run_configs
from sysinfo import get_argv
from os import get_terminal_size


def print_line():
    size = int(get_terminal_size()[0]*0.75)
    print('-'*size)


def main():

    config = times(get_argv())

    long_config = config_extractor(config)
    show_config(config)
    config.pop('long rest')

    for i in range(3):
        if i > 0:
            show_config(config)
        run_configs(config)
        print(f'Counter: {i+1}')
        print_line()

    show_config(long_config)
    run_configs(long_config)

    print('\nPomodoro is done!')
    print_line()


if __name__ == '__main__':
    main()
