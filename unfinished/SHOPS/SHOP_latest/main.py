from reader import read_files, read_language
from writer import write_data
from registration import create_registration_window
import customtkinter as CTk


class Main:
    def __init__(self):
        self.directory = "/".join(__file__.split("\\")[:-1])

        self.screen_width = CTk.CTk().winfo_screenwidth()
        self.screen_height = CTk.CTk().winfo_screenheight()

        self.win = self.create_window(self.screen_width, self.screen_height)

        CTk.CTkEntry(self.win).place()

        CTk.CTkButton(self.win).place()

        self.configures, fin_data, self.favorites, self.product_list = read_files(
            self.directory
        )
        (
            self.income,
            self.expenditure,
            self.shift_number,
            self.employs_list_names,
            self.employs_name,
        ) = fin_data
        del fin_data

        self.employs_name = self.select_employs_name(
            self.employs_name, self.employs_list_names
        )

        languages = read_language(self.directory)
        create_registration_window(
            len(self.employs_list_names),
            languages,
            int(self.screen_width / 6),
            int(self.screen_height / 2.5),
            self.win,
        )
        del languages

    def select_employs_name(
        self, current_employs_name: str, employs_list_names: list
    ) -> str:
        if len(employs_list_names) > 0:
            try:
                index = employs_list_names.index(current_employs_name) + 1
                if len(employs_list_names) <= index:
                    raise ValueError
            except ValueError:
                index = 0
        else:
            return ""

        return employs_list_names[index]

    def create_window(self, width: int, height: int) -> CTk.CTk:
        win = CTk.CTk()
        win.wm_title("")
        win.configure(fg_color="light gray")
        win.geometry(f"{width // 2}x{height // 2}+{width//4}+{height//4}")
        win.wm_protocol("WM_DELETE_WINDOW", win.quit)
        return win


if __name__ == "__main__":
    window = Main()
    write_data(
        window.directory,
        (
            window.income,
            window.expenditure,
            window.shift_number,
            window.employs_list_names,
            window.employs_name,
        ),
    )
