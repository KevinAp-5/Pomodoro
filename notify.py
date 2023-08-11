from plyer import notification
from playsound import playsound
from sys import platform


class Notify():
    def __init__(self, title='', time=0):
        self.title = title.title()
        self.time = time

    def send_notification(self):
        self.playbell()
        notification.notify(  # Pop up notification
            title=f'{self.title.title()} is done!',
            message=f'{self.time}:00 minutes is about to run.',
            app_name='Pomodoro',
            timeout=6
        )

    def done(self):
        notification.notify(
            title='Pomodoro cicle is done!',
            message="Congratulations",
            app_name='Pomodoro',
            timeout=6
        )

    @staticmethod
    def playbell():
        playsound('sounds/sound.mp3')
