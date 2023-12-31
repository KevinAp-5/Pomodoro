from plyer import notification
from playsound import playsound
from sys import platform
from os.path import realpath
import threading

class Notify():
    def __init__(self, title='', time=0):
        self.title = title.title()
        self.time = time

    def send_notification(self, title, message, timeout=6):
        threading.Thread(target=self.playbell).start()
        notification.notify(
            title=title,
            message=message,
            timeout=timeout,
            app_name='Pomodoro'
        )

    @staticmethod
    def playbell():
        path = realpath(__file__).split('/')
        path.pop(-1)
        path = '/'.join(path)
        playsound(f'{path}/sounds/sound.mp3')

