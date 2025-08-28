import customtkinter as CTk
from datetime import datetime, timedelta
import locale


def add_transaction(self):
    # создание окна создания транзакции
    win = CTk.CTkToplevel(self.win)
    win.title("Добавление")
    win.resizable(False, False)
    win.geometry("200x270+100+100")
    win.configure(fg_color=self.background_color)
    win.grab_set()
    win.iconbitmap(f"{self.directory}/icons/add.ico", f"{self.directory}/icons/add.ico")
    win.configure(icon=f"{self.directory}/icons/add.ico")
    # win.iconbitmap(f"{self.directory}/icons/add.ico")
    locale.setlocale(category=locale.LC_TIME, locale="")
    date_now = datetime.today()

    # создание поля для названия
    self.name = CTk.CTkEntry(
        win,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        placeholder_text="Название",
        text_color=self.text_color,
        placeholder_text_color=self.mode + "gray",
        font=CTk.CTkFont(size=16),
    )
    self.name.pack(fill="x", padx=10, pady=10)

    # создание поля для даты
    self.date = CTk.CTkOptionMenu(
        win,
        height=25,
        fg_color=self.background_widget_color,
        values=[
            str((date_now - timedelta(days=1)).strftime("%d %B %Y")),
            str(date_now.strftime("%d %B %Y")),
            str((date_now - timedelta(days=-1)).strftime("%d %B %Y")),
        ],
        text_color=self.text_color,
        button_color=self.background_widget_color,
        button_hover_color=self.background_activate_widget_color,
        dropdown_fg_color=self.background_widget_color,
        dropdown_hover_color=self.background_color,
        dropdown_text_color=self.text_color,
        font=CTk.CTkFont(size=16),
    )
    self.date.set(str(date_now.strftime("%d %B %Y")))
    self.date.pack(fill="x", padx=10, pady=10)

    # создание рамки для времени
    self.times_frame = CTk.CTkFrame(
        win,
        height=25,
        fg_color=self.background_color,
    )
    self.times_frame.pack(fill="x", padx=5, pady=10)

    # создание поля для часов
    self.hours = CTk.CTkEntry(
        self.times_frame,
        width=self.times_frame.cget("width") / 2 - 15,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        placeholder_text="Час",
        text_color=self.text_color,
        placeholder_text_color=self.mode + "gray",
        font=CTk.CTkFont(size=16),
    )
    self.hours.grid(column=0, row=0, padx=5)

    # создание поля для минут
    self.minutes = CTk.CTkEntry(
        self.times_frame,
        width=self.times_frame.cget("width") / 2 - 15,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        placeholder_text="Минута",
        text_color=self.text_color,
        placeholder_text_color=self.mode + "gray",
        font=CTk.CTkFont(size=16),
    )
    self.minutes.grid(column=1, row=0, padx=5)

    # создание поля для суммы
    self.amount = CTk.CTkEntry(
        win,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        placeholder_text="Сумма",
        text_color=self.text_color,
        placeholder_text_color=self.mode + "gray",
        font=CTk.CTkFont(size=16),
    )
    self.amount.pack(fill="x", padx=10, pady=10)

    # создание меню для категории
    self.category = CTk.CTkOptionMenu(
        win,
        height=25,
        fg_color=self.background_widget_color,
        values=["доход", "расход", "доход накопления", "расход накопления"],
        text_color=self.text_color,
        button_color=self.background_widget_color,
        button_hover_color=self.background_activate_widget_color,
        dropdown_fg_color=self.background_widget_color,
        dropdown_hover_color=self.background_color,
        dropdown_text_color=self.text_color,
        font=CTk.CTkFont(size=16),
    )
    self.category.pack(fill="x", padx=10, pady=10)

    # создание кнопки для сохранения
    self.save = CTk.CTkButton(
        win,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        text="Сохранить",
        text_color=self.text_color,
        hover_color=self.background_activate_widget_color,
        font=CTk.CTkFont(size=16),
        command=lambda: save(self),
    )
    self.save.pack(fill="x", padx=10, pady=10)

    win.mainloop()


def calculate(self):
    try:
        minute = int(self.minutes.get()) % 60
    except:
        minute = 0

    try:
        hour = int(self.hours.get()) + (int(self.minutes.get()) // 60)
    except:
        hour = 0

    if hour >= 24:
        minute = 0
        hour = 0

    minute = str(minute)
    hour = str(hour)

    if len(minute) == 1:
        minute = "0" + minute

    if len(hour) == 1:
        hour = "0" + hour

    self.hours.delete(0, CTk.END)
    self.hours.insert(0, hour)

    self.minutes.delete(0, CTk.END)
    self.minutes.insert(0, minute)

    del hour, minute


# сохранение транзакции
def save(self):
    calculate(self)

    # создание рамки транзакции
    frame = CTk.CTkFrame(
        self.list_frame, width=734, height=30, fg_color=self.background_widget_color
    )
    frame.pack(padx=10, pady=5)

    # добавление транзакции в список
    self.btn_list.append(
        {
            "название": self.name.get(),
            "дата": self.date.get(),
            "время": f"{self.hours.get()}:{self.minutes.get()}",
            "сумма": self.amount.get(),
            "категория": self.category.get(),
            "button": frame,
            "индекс": self.index,
        }
    )
    self.index += 1

    # размещение даты в рамке транзакции
    CTk.CTkLabel(
        frame,
        width=200,
        height=30,
        fg_color=self.background_widget_color,
        text=self.date.get(),
        text_color=self.text_color,
        font=CTk.CTkFont(size=20),
    ).place(x=0, y=0)

    # размещение названия в рамке транзакции
    CTk.CTkLabel(
        frame,
        width=250,
        height=30,
        fg_color=self.background_widget_color,
        text=self.name.get(),
        text_color=self.text_color,
        font=CTk.CTkFont(size=20),
    ).place(x=200, y=0)

    # размещение времени в рамке транзакции
    CTk.CTkLabel(
        frame,
        width=84,
        height=30,
        fg_color=self.background_widget_color,
        text=f"{self.hours.get()}:{self.minutes.get()}",
        text_color=self.text_color,
        font=CTk.CTkFont(size=20),
    ).place(x=450, y=0)

    # размещение суммы в рамке транзакции
    CTk.CTkLabel(
        frame,
        width=100,
        height=30,
        fg_color=self.background_widget_color,
        text=self.amount.get(),
        text_color=self.text_color,
        font=CTk.CTkFont(size=20),
    ).place(x=534, y=0)

    # размещение категории в рамке транзакции
    CTk.CTkLabel(
        frame,
        width=100,
        height=30,
        fg_color=self.background_widget_color,
        text=self.category.get(),
        text_color=self.text_color,
        font=CTk.CTkFont(size=20),
    ).place(x=634, y=0)
