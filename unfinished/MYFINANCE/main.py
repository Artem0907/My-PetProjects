# Импорт библиотек и файлов
from ujson import dump, load

import customtkinter as CTk
from PIL import Image

from add_trans import add_transaction
from delete_trans import delete_transaction
from edit_trans import edit_transaction
from graph import create_graphic
from sorting import sort_system

path = "/".join(__file__.split("\\")[:-1])


# главный класс
class Main:
    # конструктор
    def __init__(self, colors: dict[str, str]) -> None:
        self.directory = "/".join(__file__.split("\\")[:-1])

        # извлечь список доходов и расходов из файла
        with open(f"{self.directory}/data.json", "r", encoding="utf-8") as file:
            data: dict[str, float] = load(file)

            self.incomes = [data["доходы"]]

            self.expenses = [data["расходы"]]
            self.savings_incomes = [data["в накопления"]]
            self.savings_expenses = [data["из накоплений"]]

            self.incomes_total = float(sum(self.incomes))
            self.expenses_total = float(sum(self.expenses))
            self.total = float(self.incomes_total - self.expenses_total)

            self.incomes_savings_total = float(sum(self.savings_incomes))
            self.expenses_savings_total = float(sum(self.savings_expenses))
            self.savings_total = float(
                self.incomes_savings_total - self.expenses_savings_total
            )

            self.data = data
            del data

        # инициализация переменных в классе
        self.index = 1
        self.background_color: str = colors["background_color"]
        self.background_widget_color: str = colors["background_widget_color"]
        self.background_activate_widget_color: str = colors[
            "background_activate_widget_color"
        ]
        self.btn_list = []

        match colors.get("mode", "None").lower():
            case "dark" | "black":
                self.mode: str = "dark"
                self.text_color = "white"
            case "light" | "white":
                self.mode: str = "light"
                self.text_color: str = "black"
            case _:
                self.mode: str = "light"
                self.text_color: str = "black"

        # создание и настройка окна
        self.win = CTk.CTk()
        self.mainloop = self.win.mainloop
        self.win.title("")
        self.win.iconbitmap(f"{self.directory}/icons/main.ico")
        self.win.configure(fg_color=self.background_color)
        self.win.geometry("800x600+400+150")
        self.win.resizable(False, False)

        # создание виджетов
        self.create_frames()
        self.create_text()
        self.create_buttons()

        # create_graphic(self).mainloop()

    # создание и настройка рамок
    def create_frames(self) -> None:
        # создание рамки баланса
        self.balance_frame = CTk.CTkFrame(
            self.win,
            387.5,
            270,
            fg_color=self.background_widget_color,
            corner_radius=10,
        )
        self.balance_frame.place(x=10, y=10)

        # создание рамки настроек
        self.card_frame = CTk.CTkFrame(
            self.win,
            387.5,
            270,
            fg_color=self.background_widget_color,
            corner_radius=10,
        )
        self.card_frame.place(x=402.5, y=10)

        # создание рамки списка
        self.list_frame = CTk.CTkScrollableFrame(
            self.win,
            750,
            230,
            fg_color=self.background_widget_color,
            corner_radius=10,
        )
        self.list_frame.place(x=10, y=340)

    # создание и настройка текстовых полей
    def create_text(self) -> None:
        # создание текста баланса
        self.current_balance = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text="Баланс",
            font=CTk.CTkFont("Helvetica", 25, "bold"),
            text_color=self.text_color,
        )
        self.current_balance.place(x=10, y=5)

        # создание значения баланса
        self.current_balance_total = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text=str(self.total) + "₽",
            font=CTk.CTkFont("Helvetica", 30, "bold"),
            text_color=self.text_color,
        )
        self.current_balance_total.place(x=10, y=40)

        # создание текста доходов
        self.income_balance = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text="Доход",
            font=CTk.CTkFont("Helvetica", 20),
            text_color=self.text_color,
        )
        self.income_balance.place(x=10, y=90)

        # создание итога доходов
        self.income_balance_total = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text=str(self.incomes_total) + "₽",
            font=CTk.CTkFont("Helvetica", 20),
            text_color=self.text_color,
        )
        self.income_balance_total.place(x=10, y=120)

        # создание текста расходов
        self.outcome_balance = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text="Расход",
            font=CTk.CTkFont("Helvetica", 20),
            text_color=self.text_color,
        )
        self.outcome_balance.place(x=10, y=150)

        # создание значения расходов
        self.outcome_balance_total = CTk.CTkLabel(
            self.balance_frame,
            height=45,
            fg_color="transparent",
            text=str(self.expenses_total) + "₽",
            font=CTk.CTkFont("Helvetica", 20),
            text_color=self.text_color,
        )
        self.outcome_balance_total.place(x=10, y=180)

    # создание и настройка кнопок редактирования
    def create_buttons(self) -> None:
        # создание кнопки новой транзакции
        self.new_button = CTk.CTkButton(
            self.win,
            256.5,
            50,
            fg_color=self.background_widget_color,
            hover_color=self.background_activate_widget_color,
            image=CTk.CTkImage(
                light_image=Image.open(f"{path}/icons/add.ico"),
                dark_image=Image.open(f"{path}/icons/add.ico"),
                size=(40, 40),
            ),
            compound="left",
            text="Новая транзакция",
            text_color=self.text_color,
            command=lambda: add_transaction(self),
        )
        self.new_button.place(x=10, y=285)

        # создание кнопки редактирования транзакция
        self.edit_button = CTk.CTkButton(
            self.win,
            256.5,
            50,
            fg_color=self.background_widget_color,
            hover_color=self.background_activate_widget_color,
            image=CTk.CTkImage(
                light_image=Image.open(f"{path}/icons/edit.ico"),
                dark_image=Image.open(f"{path}/icons/edit.ico"),
                size=(40, 40),
            ),
            compound="left",
            text="Редактировать транзакцию",
            text_color=self.text_color,
            command=lambda: edit_transaction(self),
        )
        self.edit_button.place(x=271.5, y=285)

        # создание кнопки удаления транзакции
        self.delete_button = CTk.CTkButton(
            self.win,
            256.5,
            50,
            fg_color=self.background_widget_color,
            hover_color=self.background_activate_widget_color,
            image=CTk.CTkImage(
                light_image=Image.open(f"{path}/icons/delete.ico"),
                dark_image=Image.open(f"{path}/icons/delete.ico"),
                size=(40, 40),
            ),
            compound="left",
            text="Удалить транзакцию",
            text_color=self.text_color,
            command=lambda: delete_transaction(self),
        )
        self.delete_button.place(x=533, y=285)

        self.sorting_button = CTk.CTkOptionMenu(
            self.card_frame,
            width=200,
            height=50,
            fg_color=self.background_widget_color,
            values=["название", "дата", "время", "сумма", "категория"],
            text_color=self.text_color,
            button_color=self.background_widget_color,
            button_hover_color=self.background_activate_widget_color,
            dropdown_fg_color=self.background_widget_color,
            dropdown_hover_color=self.background_color,
            dropdown_text_color=self.text_color,
            dropdown_font=CTk.CTkFont(size=16),
            font=CTk.CTkFont(size=24),
            command=lambda value: sort_system(self),
        )
        self.sorting_button.place(x=10, y=10)


# проверка является ли файл не импортированным
if __name__ == "__main__":
    # создание экземпляра класса
    main = Main(
        {
            "background_color": "#006400",
            "background_widget_color": "#009600",
            "background_activate_widget_color": "#007d00",
            "mode": "dark",
        }
    )

    # запуск программы
    main.mainloop()

    incomes = main.incomes_total + sum(
        [
            (
                int(main.btn_list[i]["сумма"])
                if main.btn_list[i]["категория"] == "доход"
                and main.btn_list[i]["сумма"] != ""
                else 0
            )
            for i in range(len(main.btn_list))
        ]
    )

    outcomes = main.expenses_total + sum(
        [
            (
                int(main.btn_list[i]["сумма"])
                if main.btn_list[i]["категория"] == "расход"
                and main.btn_list[i]["сумма"] != ""
                else 0
            )
            for i in range(len(main.btn_list))
        ]
    )

    savings_incomes = main.incomes_savings_total + sum(
        [
            (
                int(main.btn_list[i]["сумма"])
                if main.btn_list[i]["категория"] == "доход накопления"
                and main.btn_list[i]["сумма"] != ""
                else 0
            )
            for i in range(len(main.btn_list))
        ]
    )

    savings_outcomes = main.expenses_savings_total + sum(
        [
            (
                int(main.btn_list[i]["сумма"])
                if main.btn_list[i]["категория"] == "расход накопления"
                and main.btn_list[i]["сумма"] != ""
                else 0
            )
            for i in range(len(main.btn_list))
        ]
    )

    data = {
        "доходы": incomes,
        "расходы": outcomes,
        "в накопления": savings_incomes,
        "из накоплений": savings_outcomes,
    }

    with open(f"{main.directory}/data.json", "w+", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)
