from plyer import notification
from playsound import playsound
from sysinfo import whereami
from sys import platform


class Notify():
    def __init__(self, title='', time=0):
        self.title = title
        self.time = time

    def send_notification(self):
        self.playbell()
        notification.notify(  # Pop up notification
            title=f'{self.title.title()} is done!',
            message=f'{self.time}:00 minutes is about to run.',
            app_name='Pomodoro',
            timeout=10
        )

    def done(self):
        notification.notify(
            title='Pomodoro cicle is done!',
            message="Congratulations",
            app_name='Pomodoro',
            timeout=10
        )

    def playbell(self):
        if 'win' in platform:
            playsound(whereami()+'\\sounds\\sound.mp3')
        else:
            playsound(whereami()+'/sounds/sound.mp3')
