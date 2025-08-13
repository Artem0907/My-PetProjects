# Импорт библиотек и файлов
from ujson import dump, load
from time import sleep
import customtkinter as CTk
import tkinter.messagebox as messagebox
from button import create_buttons, list_management
from frame import create_frames
from registration import registration_window
from widget import create_widgets
from reader import read_lang_file, read_config_file, read_data_files


# Главный класс
class Main:
    # Конструктор класса
    def __init__(self) -> None:
        # Узнаем текущую директорию папки с файлами
        self.directory = "/".join(__file__.split("\\")[:-1])

        # Узнаем ширину и высоту экрана
        self.width = CTk.CTk().winfo_screenwidth()
        self.height = CTk.CTk().winfo_screenheight()

        # создание и настройка окна
        self.win = CTk.CTk()
        self.win.title("")
        self.win.configure(fg_color="light gray")
        self.win.attributes("-toolwindow", 1)
        self.win.state("zoomed")
        self.win.geometry(f"{self.width}x{self.height}+0+0")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)
        self.running = True

        read_data_files(self)
        create_frames(self)
        create_widgets(self)
        create_buttons(self)

        if self.employs_list_names == []:
            registration_window(self)

        # Бесконечный цикл отображения окна
        while self.running:
            # Управление окном каждый цикл

            # Обновление окна
            self.win.update()
            sleep(0.05)

    def close_window(self):
        self.running = False


# Проверка на не импортирование файла
if __name__ == "__main__":
    window = Main()
