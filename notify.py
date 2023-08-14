from plyer import notification
from playsound import playsound
from sys import platform


class Notify():
    def __init__(self, title='', time=0):
        self.title = title.title()
        self.time = time

    def send_notification(self, title, message, timeout=6):
        self.playbell()
        notification.notify(
            title=title,
            message=message,
            timeout=timeout,
            app_name='Pomodoro'
        )

    @staticmethod
    def playbell():
        playsound('sounds/sound.mp3')
