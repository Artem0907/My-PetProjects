# total_percent_price = total_price * (1 + total_percent / 100)
# command=lambda product_id=product: add_button_to_list(self, product_id)


# Импорт библиотеки
import customtkinter as CTk


# Создание экземпляров кнопок
def create_buttons(self) -> None:
    self.button1 = CTk.CTkButton(
        self.navigation_frame,
        width=150,
        height=50,
        text="HOME",
        command=lambda: select_frame_by_name(self, "home"),
        fg_color="transparent",
        text_color="black",
    )
    self.button1.pack()
    self.button2 = CTk.CTkButton(
        self.navigation_frame,
        width=150,
        height=50,
        text="FRAME 2",
        command=lambda: select_frame_by_name(self, "frame 2"),
        fg_color="transparent",
        text_color="black",
    )
    self.button2.pack()
    select_frame_by_name(self, "home")
    CTk.CTkLabel(self.home_frame, text="LABEL HOME").pack()
    CTk.CTkLabel(self.frame_2, text="LABEL 2").pack()


def select_frame_by_name(self, name):
    self.button1.configure(fg_color="gray75" if name == "home" else "transparent")
    self.button2.configure(fg_color="gray75" if name == "frame 2" else "transparent")

    if name == "home":
        self.home_frame.place(x=150, y=0)
    else:
        self.home_frame.place_forget()
    if name == "frame 2":
        self.frame_2.place(x=150, y=0)
    else:
        self.frame_2.place_forget()


# Размещение кнопок
def place_button(self) -> None:
    return


# Перемещение по списку кнопок
def list_management(self) -> None:
    return


# Добавление продукта в список
def add_button_to_list(self, product_id: int) -> None:
    return


# Удаление продукта из списка
def remove_button_from_list(
    self,
    button_name: str,
) -> None:
    return
