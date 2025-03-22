import customtkinter as CTk
from datetime import datetime, timedelta
import locale


def delete_transaction(self):
    # создание окна создания транзакции
    win = CTk.CTkToplevel(self.win)
    win.title("Удаление")
    win.resizable(False, False)
    win.geometry("200x270+100+100")
    win.configure(fg_color=self.background_color)
    win.grab_set()
    win.iconbitmap(
        f"{self.directory}/icons/delete.ico", f"{self.directory}/icons/delete.ico"
    )
    win.configure(icon=f"{self.directory}/icons/add.ico")
    # win.iconbitmap(f"{self.directory}/icons/add.ico")
    locale.setlocale(category=locale.LC_TIME, locale="")
    date_now = datetime.today()

    # создание меню для категории
    self.transaction = CTk.CTkOptionMenu(
        win,
        height=25,
        fg_color=self.background_widget_color,
        values=[
            str(self.btn_list[index]["индекс"])
            for index in range(0, len(self.btn_list), 1)
        ],
        text_color=self.text_color,
        button_color=self.background_widget_color,
        button_hover_color=self.background_activate_widget_color,
        dropdown_fg_color=self.background_widget_color,
        dropdown_hover_color=self.background_color,
        dropdown_text_color=self.text_color,
        font=CTk.CTkFont(size=16),
    )
    self.transaction.pack(fill="x", padx=10, pady=10)

    # создание кнопки для сохранения
    self.delete = CTk.CTkButton(
        win,
        height=25,
        fg_color=self.background_widget_color,
        border_width=0,
        text="Сохранить",
        text_color=self.text_color,
        hover_color=self.background_activate_widget_color,
        font=CTk.CTkFont(size=16),
        command=lambda: delete(self, self.transaction.get()),
    )
    self.delete.pack(fill="x", padx=10, pady=10)

    win.mainloop()


def delete(self, index):
    for index in range(0, len(self.btn_list), 1):
        if str(self.btn_list[index]["индекс"]) == index:
            self.btn_list[index]["button"].destroy()
