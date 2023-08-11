import pyautogui
from plyer import notification
from time import sleep

notification.notify(
    title='Test will start in 5 seconds!',
    timeout=7,
    message='comment in code:\ninterval()\nnotification()'
)

sleep(7)
pyautogui.PAUSE = 0.1
for _ in range(8):
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('k')
    pyautogui.press('enter')
    sleep(0.1)
