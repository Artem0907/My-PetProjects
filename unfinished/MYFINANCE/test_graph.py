import customtkinter as CTk


def add_transaction(self):
    win = CTk.CTkToplevel(self.win)
    win.title("Добавление")
    win.resizable(False, False)
    win.geometry("1200x700+100+100")
    win.configure(fg_color=self.background_color)
    win.grab_set()
    win.iconbitmap(self.icon)

    canvas = CTk.CTkCanvas(win, width=1000, height=700, bg="black")
    canvas.pack()

    def draw(x_l, y_b, x_r, y_t):
        dx = 1000 / (x_r - x_l)
        dy = 700 / (y_t - y_b)

        cx = -x_l * dx
        cy = y_t * dy

        canvas.create_line(0, cy, 1000, cy, fill="light green")
        canvas.create_line(cx, 0, cx, 700, fill="light green")

        x_step = (x_r - x_l) / 10
        x = x_l
        while x <= x_r:
            x_canvas = (x - x_l) * dx
            canvas.create_line(x_canvas, 0, x_canvas, 1000, fill="white")
            canvas.create_text(
                x_canvas,
                cy + 15,
                text=str(round(x, 1)),
                font=CTk.CTkFont("Verdana", 9),
                fill="white",
            )

            x += x_step

        y_step = (y_t - y_b) / 10
        y = y_t
        while y >= y_b:
            y_canvas = (y - y_t) * dy
            canvas.create_line(0, -y_canvas, 1500, -y_canvas, fill="white")
            canvas.create_text(
                cx + 25,
                -y_canvas,
                text=str(round(y, 1)),
                font=CTk.CTkFont("Verdana", 9),
                fill="white",
            )

            y -= y_step

    draw(-10, -20, 100, 200)

    win.mainloop()
