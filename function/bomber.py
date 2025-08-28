from typing import NoReturn
from pyautogui import typewrite
from time import sleep
from keyboard import is_pressed, press_and_release


def bomber(text: str) -> NoReturn:
    bombing = False
    while True:
        if is_pressed("alt+s"):
            bombing = not bombing
            print("Bombing...")
            sleep(5)
        if bombing:
            typewrite(text)
            press_and_release("ctrl+enter")
            sleep(0.01)


if __name__ == "__main__":
    bomber(input("Enter text: "))
