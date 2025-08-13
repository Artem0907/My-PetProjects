# Импорт библиотек и файлов
import customtkinter as CTk


# создание кнопок списка продуктов
def create_button(self) -> None:
    width = int((self.button_label.cget("width") // 5) - 5)
    height = int((self.button_label.cget("height") // 10) - 5)

    self.btn1 = CTk.CTkButton(
        self.button_label,
        width,
        height,
        text_color=self.background_button_text_color,
        text=self.products[0][0],
        font=CTk.CTkFont("Helvetica", 15),
        bg_color=self.background_color,
        fg_color=self.background_button_color,
        hover_color=self.background_button_color,
        corner_radius=0,
        command=lambda: self.button_click(self.btn1),
    )
    self.btn2 = CTk.CTkButton(
        self.button_label,
        width,
        height,
        text_color=self.background_button_text_color,
        text=self.products[1][0],
        font=CTk.CTkFont("Helvetica", 15),
        bg_color=self.background_color,
        fg_color=self.background_button_color,
        hover_color=self.background_button_color,
        corner_radius=0,
        command=lambda: self.button_click(self.btn1),
    )
    self.btn3 = CTk.CTkButton(
        self.button_label,
        width,
        height,
        text_color=self.background_button_text_color,
        text=self.products[2][0],
        font=CTk.CTkFont("Helvetica", 15),
        bg_color=self.background_color,
        fg_color=self.background_button_color,
        hover_color=self.background_button_color,
        corner_radius=0,
        command=lambda: self.button_click(self.btn1),
    )
