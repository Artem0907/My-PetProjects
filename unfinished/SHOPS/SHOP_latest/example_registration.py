import customtkinter as CTk


def create_registration_window(
    len_list_names: int,
    language: dict,
    width: int,
    height: int,
    window: CTk.CTk,
) -> None:
    global registration_win
    allow_login = True if len_list_names else False
    allow_login = True

    registration_win = registration_window(width, height)
    registration_win.focus()

    if allow_login:
        global cursor_button, widgets
        widgets = create_registration_widgets(
            registration_win, width - 20, height / 3 - 20, width, height
        )
        cursor_button = widgets[0][0]
        cursor_button.place(x=0, y=0)
        place_widgets(widgets[1], 10, 10)
        place_widgets(widgets[2], 10, 10)
    else:
        widgets = create_registration_widgets(registration_win)
        place_widgets(widgets, 10, 10)

    registration_win.mainloop()
    window.mainloop()


def button():
    global cursor_button, widgets, registration_win
    cursor_button.place_forget()
    cursor_button = widgets[0][1] if cursor_button == widgets[0][0] else widgets[0][0]
    cursor = widgets[1][0] if cursor_button == widgets[0][0] else widgets[2][0]
    cursor.focus()
    registration_win.title("Регистрация" if cursor_button == widgets[0][0] else "Вход")
    cursor_button.place(x=0, y=0)


def create_registration_widgets(
    window: CTk.CTk,
    widget_width: int,
    widget_height: int,
    frame_width: int,
    frame_height: int,
) -> list | tuple:
    registration_frame = CTk.CTkFrame(
        window, frame_width, frame_height, corner_radius=0, fg_color="light gray"
    )
    login_frame = CTk.CTkFrame(
        window, frame_width, frame_height, corner_radius=0, fg_color="light gray"
    )

    registration_label = CTk.CTkEntry(
        registration_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        placeholder_text="Регистрация",
    )
    login_label = CTk.CTkEntry(
        login_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        placeholder_text="Вход",
    )

    registration_last_name_label = CTk.CTkLabel(
        registration_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        text="РЕГИСТРАЦИЯ",
    )
    registration_button = CTk.CTkButton(
        registration_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        text="логин",
        command=button,
    )

    login_last_name_label = CTk.CTkLabel(
        login_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        text="ЛОГИН",
    )
    login_button = CTk.CTkButton(
        login_frame,
        width=widget_width,
        height=widget_height,
        corner_radius=0,
        text="регистрация",
        command=button,
    )

    return (
        [registration_frame, login_frame],
        [registration_label, registration_last_name_label, registration_button],
        [login_label, login_last_name_label, login_button],
    )


def create_login_widgets(
    window: CTk.CTk, widget_width: int, widget_height: int
) -> list | tuple:
    ...


def place_widgets(
    widget_list: list | tuple, pad_x: float | int, pad_y: float | int
) -> None:
    id_row = 0
    max_column = 1
    for widget in widget_list:
        if type(widget) in [tuple, list]:
            max_column = max(max_column, len(widget))

    for widget in widget_list:
        if type(widget) in [tuple, list]:
            for id_widget in range(0, len(widget)):
                # если не 1 и меньше самого большого то по другому
                # и попытаться сделать чтобы норм отображались нечетные на пару с четными
                widget[id_widget].grid(
                    column=id_widget,
                    columnspan=max_column // len(widget),
                    row=id_row,
                    padx=pad_x / len(widget),
                    pady=pad_y,
                )
        else:
            widget.grid(
                column=0, columnspan=max_column, row=id_row, padx=pad_x, pady=pad_y
            )
        id_row += 1


def registration_window(width: int, height: int) -> CTk.CTk:
    win = CTk.CTk()
    win.title("РЕГИСТРАЦИЯ")
    win.configure(fg_color="light gray")
    win.geometry(f"{width}x{height}")
    win.resizable(False, False)
    win.protocol(
        "WM_DELETE_WINDOW", lambda window=win: (window.destroy(), window.quit())
    )
    return win
