import customtkinter as CTk


# создание графиков
def create_graphic(self):
    # создание окна графиков
    graph_win = CTk.CTk()
    graph_win.title("График")
    graph_win.configure(width=780, height=560)
    graph_win.resizable(False, False)
    graph_win.configure(fg_color=self.background_color)
    graph_win.iconbitmap(f"{self.directory}/icons/main.ico")

    # координаты полосок по x
    x = [0, len(self.data)]

    # координаты размещения полосок по x
    x_place = [x_coords for x_coords in range(0, 561, int(560 / x[1]))][1:-1]
    canvas = CTk.CTkCanvas(
        graph_win, width=560, height=560, bg=self.background_widget_color
    )
    canvas.place(x=220, y=0)

    # размещение полосок по x
    for x_pl in x_place:
        canvas.create_line(x_pl, 0, x_pl, 560, fill="light grey")

    # координаты полосок по y
    self.incomes = [1, 2, 3]
    self.expenses = [1, 2, 3]
    y_min = float(max(max(self.expenses), max(self.savings_expenses)))
    y_max = float(max(max(self.incomes), max(self.savings_incomes)))
    y = [0.0, *self.incomes, *self.savings_incomes]
    y = list(set(y))
    y.sort()
    y = y[1:-1]

    # координаты размещения полосок по y
    y_place = [0.0, *[280 - ((280 / y_max) * i) for i in y], 560.0]
    y_place = list(set(y_place))
    y_place.sort()
    y_place = y_place[1:-1]

    # размещение минимальной полоски по y
    canvas.create_line(0, 280, 560, 280, fill="white")

    # размещение полосок по y
    for y_pl in y_place:
        canvas.create_line(0, y_pl, 560, y_pl, fill="dark grey")

    # размещение максимальной полоски по y
    canvas.create_line(0, 280, x_place[0], y_place[-1], fill="red")
    j = len(y_place) - 1

    # размещение полосок по x и y
    for i in range(len(y_place) - 1):
        j -= 1
        canvas.create_line(
            x_place[i], y_place[j + 1], x_place[i + 1], y_place[j], fill="red"
        )
    canvas.create_line(x_place[-1], y_place[0], 560, 0, fill="red")

    # вторые координаты полосок по y
    y = [0.0, *self.expenses, *self.savings_expenses]
    y = list(set(y))
    y.sort()
    y = y[1:-1]

    # координаты вторых координат полосок по y
    y_place = [0.0, *[280 + ((280 / y_min) * i) for i in y], 560.0]
    y_place = list(set(y_place))
    y_place.sort()
    y_place = y_place[1:-1]

    # размещение вторых координат полосок по y
    for y_pl in y_place:
        canvas.create_line(0, y_pl, 560, y_pl, fill="dark grey")

    # создание минимальной полоски по второй y
    canvas.create_line(0, 280, x_place[0], y_place[0], fill="red")
    j = -1

    # создание полосок по второй y
    for i in range(len(y_place) - 1):
        j += 1
        canvas.create_line(
            x_place[i], y_place[j], x_place[i + 1], y_place[j + 1], fill="red"
        )

    # создание максимальной полоски по второй y
    canvas.create_line(x_place[-1], y_place[-1], 560, 560, fill="red")

    # возврат окна графиков
    return graph_win
