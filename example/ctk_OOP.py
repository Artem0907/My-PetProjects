import customtkinter as CTk


class Main:
    def __init__(self) -> None:
        self.win = CTk.CTk()
        self.win.title("EXAMPLE")
        self.win.resizable(False, False)
        self.win.geometry("500x500+100+100")
        self.win.configure(fg_color="white")
        # self.win.iconbitmap("./icon.ico")


if __name__ == "__main__":
    Main().win.mainloop()
