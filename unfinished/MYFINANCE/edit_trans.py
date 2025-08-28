import customtkinter as CTk


def edit_transaction(self):
    win = CTk.CTkToplevel(self.win)
    win.title("Редактирование")
    win.resizable(False, False)
    win.geometry("300x400+100+100")
    win.configure(fg_color=self.background_color)
    win.grab_set()
    win.iconbitmap(f"{self.directory}/icons/edit.ico")

    win.mainloop()
