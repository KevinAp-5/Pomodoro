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
            resume_pomodoro = self.user_input.get_answer()
            if resume_pomodoro == 'y':
                print('Continuing.')
                break
            elif resume_pomodoro == 'n':
                print('\nBye!')
                exit()
            elif resume_pomodoro == 'k':
                print('Killed.')
                return 'kill'
            elif resume_pomodoro == 'r':
                print('Restarted')
                return False
            else:
                print('Invalid answer! Use Yes or No.')
                self.reset()
                continue
        self.reset()

    def reset(self):
        self.user_input = Get_input()
