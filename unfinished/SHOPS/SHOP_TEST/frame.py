# Импорт библиотеки
import customtkinter as CTk


# Создание экземпляров рамок
def create_frames(self) -> None:
    self.navigation_frame = CTk.CTkFrame(
        self.win, width=150, height=self.height, corner_radius=0
    )
    self.home_frame = CTk.CTkFrame(
        self.win, width=self.width - 150, height=self.height, corner_radius=0
    )
    self.frame_2 = CTk.CTkFrame(
        self.win, width=self.width - 150, height=self.height, corner_radius=0
    )
    place_frames(self)


# Размещение рамок
def place_frames(self) -> None:
    self.navigation_frame.place(x=0, y=0)
