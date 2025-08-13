# Импорт библиотек и файлов
from json import dump, load
from tkinter.messagebox import Message

import customtkinter as CTk
from button import create_button
from products import create_check_box


# главный класс
class Main:
    # конструктор
    def __init__(
        self, colors: tuple[str, str, str, str, str], path: str
    ) -> None:
        # извлечь список продуктов из файла
        with open(f"{path}/products.json", "r", encoding="utf-8") as file:
            self.products = load(file)
        # извлечь список доходов и расходов из файла
        with open(f"{path}/data.json", "r", encoding="utf-8") as file:
            data = load(file)
            self.income = data["доход"]
            self.expenditure = data["расход"]
            self.shift_number = data["номер смены"] + 1
            self.order_number = data["номер заказа"] + 1
            self.names = data["имена сотрудников"]
            res = False
            for i in self.names:
                if res:
                    self.employs_name = i
                    break
                if i == data["имя сотрудника"]:
                    res = True
            else:
                if len(self.names) >= 1:
                    self.employs_name = self.names[0]
            del data

        # инициализация переменных в классе
        self.background_color: str = colors[0]
        self.background_list_color: str = colors[1]
        self.text_color: str = colors[2]
        self.background_button_color: str = colors[3]
        self.background_button_text_color: str = colors[4]
        self.check_box_list: dict[int] = {}
        self.number_price_label = 1
        self.number_data_list: list[CTk.CTkLabel] = []
        self.path = path

        # создание и настройка окна
        self.win = CTk.CTk()
        self.win.title("")
        self.win.configure(fg_color=self.background_color)
        self.win.attributes("-toolwindow", 1)
        self.width: int = self.win.winfo_screenwidth()
        self.height: int = self.win.winfo_screenheight()
        self.win.state("zoomed")
        self.win.geometry(f"{self.width}x{self.height}+0+0")
        # self.win.resizable(False, False)

        # создание и настройка виджетов
        self.create_label()
        self.price_data_list_width = (
            float(self.price_list_label.cget("width")) / 17
        )
        self.price_data_list_height = (
            float(self.price_list_label.cget("height")) / 15
        )
        create_button(self)
        self.create_heading()
        # список кнопок
        self.but: list[CTk.CTkButton] = [self.btn1, self.btn2, self.btn3]
        # позиции кнопок
        self.position: list[tuple[int, int]] = [
            (c, r)
            for r in range(
                5,
                int((self.button_label.cget("height"))),
                int((self.button_label.cget("height") // 10)),
            )
            for c in range(
                5,
                int((self.button_label.cget("width"))),
                int((self.button_label.cget("width") // 5)),
            )
        ]

        # создание виджетов
        self.place_button()
        self.create_total_price()
        self.create_data_labels()
        self.none()

    # создание и размещение рамок
    def create_label(self) -> None:
        # создание и размещение рамки кнопок
        self.button_label = CTk.CTkLabel(
            self.win,
            (self.width / 2.5),
            (self.height / 1.5),
            bg_color=self.background_color,
            text="",
        )
        self.button_label.place(x=((self.width - self.width / 2.5) - 5), y=5)

        # создание и размещение рамки
        self.label_2 = CTk.CTkLabel(
            self.win,
            (self.width / 2.5),
            ((self.height - self.height / 1.5) - 40),
            bg_color=self.background_color,
            text="",
        )
        self.label_2.place(
            x=((self.width - self.width / 2.5) - 5),
            y=((self.height / 1.5) + 10),
        )

        # создание и размещение рамки
        self.data_label = CTk.CTkLabel(
            self.win,
            ((self.width - (self.width / 2.5)) - 15),
            50,
            bg_color=self.background_color,
            text="",
        )
        self.data_label.place(x=5, y=5)

        # создание и размещение рамки данных списка продуктов
        self.price_data_list_label = CTk.CTkLabel(
            self.win,
            ((self.width - (self.width / 2.5)) - 16),
            20,
            fg_color=self.background_list_color,
            corner_radius=0,
            text="",
        )
        self.price_data_list_label.place(x=5, y=60)

        # создание и размещение рамки списка продуктов
        self.price_list_label = CTk.CTkScrollableFrame(
            self.win,
            ((self.width - (self.width / 2.5)) - 32),
            ((self.height / 1.5) - 74),
            fg_color=self.background_list_color,
            corner_radius=0,
        )
        self.price_list_label.place(x=5, y=79)

        # создание и размещение рамки очередности продуктов
        self.price_number_label = CTk.CTkLabel(
            self.price_list_label,
            width=self.price_data_list_label.cget("width") / 17 * 2,
            fg_color=self.background_list_color,
            corner_radius=0,
            text="",
        )
        self.price_number_label.grid(column=0, row=0)

        # создание и размещение рамки данных продуктов
        self.price_data_label = CTk.CTkLabel(
            self.price_list_label,
            width=150,
            fg_color=self.background_list_color,
            corner_radius=0,
            text="",
        )
        self.price_data_label.grid(column=1, row=0)

        # создание и размещение рамки
        self.label_5 = CTk.CTkLabel(
            self.win,
            ((self.width - (self.width / 2.5)) - 15),
            ((self.height - self.height / 1.5) - 40),
            bg_color=self.background_color,
            text="",
        )
        self.label_5.place(x=5, y=((self.height / 1.5) + 10))

    # размещение кнопок списка продуктов
    def place_button(self) -> None:
        for pos in range(3):
            self.but[pos].place(
                x=self.position[pos][0], y=self.position[pos][1]
            )

    # обработка кликов на кнопку
    def button_click(self, button: CTk.CTkButton) -> None:
        create_check_box(self, button.cget("text"))

    # создание и размещение данных списка продуктов
    def create_heading(self) -> None:
        # создание и размещение нумерации продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 2,
            height=20,
            fg_color=self.background_list_color,
            text="№",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=0, y=0)

        # создание и размещение наименований продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 4,
            height=20,
            fg_color=self.background_list_color,
            text="наименование",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 2, y=0)

        # создание и размещение количества продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 2,
            height=20,
            fg_color=self.background_list_color,
            text="кол-во",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 6, y=0)

        # создание и размещение веса продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 3,
            height=20,
            fg_color=self.background_list_color,
            text="вес",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 8, y=0)

        # создание и размещение цены продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 2,
            height=20,
            fg_color=self.background_list_color,
            text="цена",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 11, y=0)

        # создание и размещение суммы цен продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 2,
            height=20,
            fg_color=self.background_list_color,
            text="сумма",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 13, y=0)

        # создание и размещение кнопок удаления продуктов
        CTk.CTkLabel(
            self.price_data_list_label,
            width=self.price_data_list_width * 1.5,
            height=20,
            fg_color=self.background_list_color,
            text="удалить",
            font=CTk.CTkFont(weight="bold"),
            text_color=self.text_color,
            corner_radius=0,
        ).place(x=self.price_data_list_width * 15, y=0)

    # создание и размещение суммы цен продуктов
    def create_total_price(self) -> None:
        # создание и размещение рамки итоговых сумм
        self.main_total_price_label = CTk.CTkLabel(
            self.label_5,
            width=400,
            height=65,
            text="",
            bg_color=self.background_list_color,
        )
        self.main_total_price_label.place(x=0, y=10)

        # создание и размещение итого со скидкой
        self.total_price = CTk.CTkLabel(
            self.main_total_price_label,
            width=185,
            height=25,
            fg_color=self.background_color,
            text="Итого без скидки: 0.0",
            text_color=self.text_color,
        )
        self.total_price.place(x=10, y=35)

        # создание и размещение скидки
        self.total_percent = CTk.CTkLabel(
            self.main_total_price_label,
            width=185,
            height=25,
            fg_color=self.background_color,
            text="Скидка: 10%",
            text_color=self.text_color,
        )
        self.total_percent.place(x=205, y=35)

        # создание и размещение итого без скидки
        self.total_percent_price = CTk.CTkLabel(
            self.main_total_price_label,
            width=185,
            height=25,
            fg_color=self.background_color,
            text="Итого: 0",
            font=CTk.CTkFont(size=15, weight="bold"),
            text_color=self.text_color,
        )
        self.total_percent_price.place(x=10, y=5)

        # создание и размещение итого без скидки
        self.total_weight = CTk.CTkLabel(
            self.main_total_price_label,
            width=185,
            height=25,
            fg_color=self.background_color,
            text="Вес: 0",
            font=CTk.CTkFont(size=15, weight="bold"),
            text_color=self.text_color,
        )
        self.total_weight.place(x=205, y=5)

    def create_data_labels(self) -> None:
        self.shift_number_label = CTk.CTkLabel(
            self.data_label,
            100,
            40,
            text=self.shift_number,
            text_color=self.text_color,
        )
        self.shift_number_label.place(x=5, y=5)

        self.shift_name_label = CTk.CTkLabel(
            self.data_label,
            100,
            40,
            text=self.employs_name,
            text_color=self.text_color,
        )
        self.shift_name_label.place(x=110, y=5)

        self.order_number_label = CTk.CTkLabel(
            self.data_label,
            100,
            40,
            text=self.order_number,
            text_color=self.text_color,
        )
        self.order_number_label.place(x=215, y=5)

    #! NONE
    def none(self) -> None:
        CTk.CTkButton(self.label_2, command=self.revenue_calculation).place(
            x=10, y=10
        )

    # создание окна выручки
    def revenue_calculation(self):
        # создание модального окна
        self.revenue_win = CTk.CTkToplevel(self.win)
        self.revenue_win.title("Выручка")
        self.revenue_win.configure(fg_color=self.background_color)
        self.revenue_win.grab_set()
        self.revenue_win.geometry("300x100")
        self.revenue_win.resizable(False, False)

        def conclusion():
            # если заполнено поле процентов
            try:
                # обновление текста выручки
                percent_revenue_price = round(
                    float(self.total_percent_price.cget("text").split(": ")[1])
                    / 100
                    * float(self.percent_revenue.get()),
                    2,
                )
            except ValueError:
                percent_revenue_price = 0.00

            Message(
                title="Итог",
                message=f"Выручка: {percent_revenue_price}",
            ).show()
            self.revenue_win.destroy()

        # создание и размещение процентов
        self.percent_revenue = CTk.CTkEntry(
            self.revenue_win,
            width=290,
            height=40,
            placeholder_text="% от доходов",
            font=CTk.CTkFont(size=22),
        )
        self.percent_revenue.place(x=5, y=5)

        # создание и размещение кнопки подсчета
        self.total_percent_revenue = CTk.CTkButton(
            self.revenue_win,
            width=130,
            height=30,
            fg_color="#FFFFFF",
            hover_color="#AFDAFC",
            border_width=2,
            border_color="#6B90D9",
            border_spacing=0,
            corner_radius=0,
            text="Подсчет",
            text_color="#000000",
            command=conclusion,
        )
        self.total_percent_revenue.place(x=10, y=60)

        self.cancel_revenue = CTk.CTkButton(
            self.revenue_win,
            width=130,
            height=30,
            fg_color="#FFFFFF",
            hover_color="#AFDAFC",
            border_width=2,
            border_color="#6B90D9",
            border_spacing=0,
            corner_radius=0,
            text="Отмена",
            text_color="#000000",
            command=self.revenue_win.destroy,
        )
        self.cancel_revenue.place(x=160, y=60)

        self.revenue_win.mainloop()


# проверка является ли файл не импортированным
if __name__ == "__main__":
    main = Main(
        ("light grey", "white", "black", "black", "yellow"),
        "/".join(__file__.split("\\")[:-1]),
    )
    # запуск программы
    main.win.mainloop()
    main.income += float(main.total_percent_price.cget("text").split(": ")[1])

    # запись финансов в файл
    with open(
        "/".join(__file__.split("\\")[:-1]) + "/data.json",
        "w",
        encoding="utf-8",
    ) as file:
        dump(
            {
                "доход": round(float(main.income), 2),
                "расход": round(float(main.expenditure), 2),
                "итог": round(
                    float(float(main.income) - float(main.expenditure)), 2
                ),
                "номер смены": main.shift_number,
                "номер заказа": main.order_number,
                "имя сотрудника": main.employs_name,
                "имена сотрудников": main.names,
            },
            file,
            ensure_ascii=False,
        )
