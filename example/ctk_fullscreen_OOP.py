import customtkinter as CTk


class Main:
    def __init__(self) -> None:
        self.win = CTk.CTk()
        self.win.title("EXAMPLE")
        self.win.configure(fg_color="white")
        self.win.attributes("-toolwindow", 1)
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()
        self.win.state("zoomed")
        self.win.geometry(f"{self.width}x{self.height}+0+0")
        self.win.resizable(False, False)
        # self.win.iconbitmap("./icon.ico")


if __name__ == "__main__":
    Main().win.mainloop()
