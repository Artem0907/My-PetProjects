# Импорт библиотек и файлов
from ujson import dump, load
import customtkinter as CTk
from tkinter.messagebox import Message
from button import create_buttons, list_management
from frame import create_frames
from widget import create_widgets


# Главный класс
class Main:
    # Конструктор класса
    def __init__(self, colors: dict[str, str] = {}) -> None:
        # Установка директории приложения
        self.directory = "/".join(__file__.split("\\")[:-1])

        # Извлечение списка продуктов из файла
        with open(f"{self.directory}/products.json", "r", encoding="utf-8") as file:
            self.products: list[list[str, int, float, float]] = load(file)

        # Извлечение бюджета из файла
        with open(f"{self.directory}/data.json", "r", encoding="utf-8") as file:
            file_data: dict = load(file)
            self.income: float = round(float(file_data.get("доход", 0)), 2)
            self.expenditure: float = round(float(file_data.get("расход", 0)), 2)
            self.shift_number: int = int(file_data.get("номер смены", 0)) + 1
            self.employs_names_list: list[str] = file_data.get("список сотрудников", [])
            self.employs_name: str = file_data.get("сотрудник", "")
            del file_data

        # Установка текущего сотрудника
        if (
            len(self.employs_names_list) == 0
            or self.employs_name is None
            or self.employs_name not in self.employs_names_list
        ):
            self.employs_name = ""
        else:
            if self.employs_name == self.employs_names_list[-1]:
                self.employs_name = self.employs_names_list[0]
            else:
                cursor = self.employs_names_list.index(self.employs_name)
                self.employs_name = self.employs_names_list[cursor + 1]
                del cursor

        # Инициализация цветов
        self.background_window_color: str = colors.get(
            "background_window", "light grey"
        )
        self.background_button_color: str = colors.get("background_button", "black")
        self.background_active_button_color: str = colors.get(
            "background_active_button", self.background_button_color
        )
        self.background_list_color: str = colors.get("background_list", "white")
        self.window_text_color: str = colors.get("window_text", "black")
        self.button_text_color: str = colors.get("button_text", "white")
        self.list_text_color: str = colors.get("list_text", "black")

        # Создание и настройка окна
        self.win = CTk.CTk()
        self.win.title("")
        self.win.configure(fg_color=self.background_window_color)
        self.win.attributes("-toolwindow", 1)

        # Инициализация размеров окна
        self.width: int = self.win.winfo_screenwidth()
        self.height: int = self.win.winfo_screenheight()

        # Установка значений размеров окна
        self.win.state("zoomed")
        self.win.geometry(f"{self.width}x{self.height}+0+0")
        self.win.resizable(False, False)

        # Создание рамок
        create_frames(self)

        # Размещение кнопок продуктов
        create_buttons(self)

        # Создание виджетов для рамок
        create_widgets(self)

        # Создание и размещение кнопок управления списком продуктов
        list_management(self)


# Проверка на не импортирование файла
if __name__ == "__main__":
    colors = {}
    window = Main(colors)
    # Запуск программы
    window.win.mainloop()
    # window.income += float(window.total_percent_price.cget("text").split(": ")[1])

    # Запись бюджета в файл
    with open(f"{window.directory}/data.json", "w", encoding="utf-8") as file:
        dump(
            {
                "доход": window.income,
                "расход": window.expenditure,
                "номер смены": window.shift_number,
                "список сотрудников": window.employs_names_list,
                "сотрудник": window.employs_name,
            },
            file,
            ensure_ascii=False,
        )
