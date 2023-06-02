from pomodoro import times, config_extractor, show_config
from pomodoro import run_long_config, run_normal_config
from sysinfo import get_argv


def main():
    config = times(get_argv())

    long_config = config_extractor(config)
    show_config(config)
    config.pop('long rest')

    for i in range(3):
        if i > 0:
            show_config(config)
        run_normal_config(config)
        print(f'Counter: {i+1}')
        print('-'*50)

    show_config(long_config)
    run_long_config(long_config)

    print('\nPomodoro is done!')
    print('-' * 50)


if __name__ == '__main__':
    main()
