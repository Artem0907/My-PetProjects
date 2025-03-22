import customtkinter as CTk


win = CTk.CTk()
win.title("EXAMPLE")
win.resizable(False, False)
win.geometry("500x500+100+100")
win.configure(fg_color="white")
# win.iconbitmap("./icon.ico")


if __name__ == "__main__":
    win.mainloop()
