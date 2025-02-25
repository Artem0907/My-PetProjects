import customtkinter as CTk


win = CTk.CTk()
win.title("EXAMPLE")
win.configure(fg_color="white")
win.attributes("-toolwindow", 1)
width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.state("zoomed")
win.geometry(f"{width}x{height}+0+0")
win.resizable(False, False)
# win.iconbitmap("./icon.ico")


if __name__ == "__main__":
    win.mainloop()
