class Get_input():
    def __init__(self):
        self.text = '\nDo you want to continue? [Y/n]\n>>> '

    def get_answer(self):
        while True:
            try:
                self.text = input(self.text).strip().lower()[0]
            except KeyboardInterrupt:
                exit()
            except IndexError:
                continue

            if self.text:
                return self.text


class Keyboard():
    def __init__(self):
        self.user_input = Get_input()

    def treat_input(self):
        while True:
            match self.user_input.get_answer():
                case 'y':  # Yes
                    print('Continuing.')
                    break
                case 'n':  # No
                    print('\nBye!')
                    exit()
                case 'k':  # Kill
                    print('Killed.')
                    return 'kill'
                case 'r':  # Restart
                    print('Restarted.')
                    return False
                case 'g':  # Go to time
                    return self.get_time()
                case _:    # Else
                    print('Invalid answer! Use Yes or No.')
                    self.reset()
                    continue
        self.reset()

    def reset(self):
        self.user_input = Get_input()

    def get_time(self):
        time = input('What time you stopped at:\n>>> ')
        if ':' in time:
            time = [int(x) for x in time.split(':')]
            minutes = time[0]
            seconds = time[1]
            time = (minutes*60) + seconds
            return time
        return int(time)*60

