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
