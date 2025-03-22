import customtkinter as CTk


def create_registration_window(
    len_list_names: int,
    language: dict,
    width: float | int,
    height: float | int,
    window: CTk.CTk,
) -> None:
    allow_registration = True if len_list_names else False
    registration_win = registration_window(width, height)
    registration_win.focus()

    widgets = (
        create_registration_widgets(window, registration_win, width, height / 15)
        if allow_registration
        else create_login_widgets(window, registration_win, width, height / 15)
    )
    place_widgets(widgets, width / 8, height / 30)

    registration_win.mainloop()


def create_registration_widgets(
    main_window: CTk.CTk, window: CTk.CTk, width: float, height: float
) -> tuple[CTk.CTkEntry | CTk.CTkButton | CTk.CTkLabel]:
    login_label = CTk.CTkLabel(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        text="Логин",
        text_color="black",
        anchor="sw",
    )
    password_label = CTk.CTkLabel(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        text="Пароль",
        text_color="black",
        anchor="sw",
    )
    last_name_label = CTk.CTkLabel(
        window,
        width=width / 2 - width / 9,
        height=height,
        corner_radius=0,
        text="Фамилия",
        text_color="black",
        anchor="sw",
    )
    first_name_label = CTk.CTkLabel(
        window,
        width=width / 2 - width / 9,
        height=height,
        corner_radius=0,
        text="Имя",
        text_color="black",
        anchor="sw",
    )
    label_label = CTk.CTkLabel(
        window,
        width=width - width / 9,
        height=height / 6,
        corner_radius=0,
        text="",
        text_color="black",
    )
    login_entry = CTk.CTkEntry(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        placeholder_text="логин",
        show=None,
        text_color="black",
    )
    password_entry = CTk.CTkEntry(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        placeholder_text="пароль",
        show="*",
        text_color="black",
    )
    last_name_entry = CTk.CTkEntry(
        window,
        width=width / 2 - width / 9,
        height=height,
        corner_radius=0,
        placeholder_text="фамилия",
        show=None,
        text_color="black",
    )
    first_name_entry = CTk.CTkEntry(
        window,
        width=width / 2 - width / 9,
        corner_radius=0,
        placeholder_text="имя",
        show=None,
        text_color="black",
    )
    entry_label = CTk.CTkLabel(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        text="",
        text_color="black",
    )
    next_button = CTk.CTkButton(
        window,
        width=width - width / 9,
        height=height,
        corner_radius=0,
        text="Далее",
        text_color="black",
        command=lambda: next_command(
            main_window, window, login_entry.get(), password_entry.get()
        ),
    )
    return (
        (last_name_label, first_name_label),
        label_label,
        (last_name_entry, first_name_entry),
        label_label,
        login_label,
        login_entry,
        label_label,
        password_label,
        password_entry,
        entry_label,
        next_button,
    )


def create_login_widgets(
    main_window: CTk.CTk, window: CTk.CTk, width: float, height: float
) -> tuple[CTk.CTkEntry | CTk.CTkButton | CTk.CTkLabel]:
    login_label = CTk.CTkLabel(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        text="Логин",
        text_color="black",
        anchor="sw",
    )
    password_label = CTk.CTkLabel(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        text="Пароль",
        text_color="black",
        anchor="sw",
    )
    label_label = CTk.CTkLabel(
        window,
        width=width - width / 6,
        height=height / 2,
        corner_radius=0,
        text="",
        text_color="black",
    )
    login_entry = CTk.CTkEntry(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        placeholder_text="логин",
        show=None,
        text_color="black",
    )
    password_entry = CTk.CTkEntry(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        placeholder_text="пароль",
        show="*",
        text_color="black",
    )
    entry_label = CTk.CTkLabel(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        text="",
        text_color="black",
    )
    next_button = CTk.CTkButton(
        window,
        width=width - width / 6,
        height=height,
        corner_radius=0,
        text="Далее",
        text_color="black",
        command=lambda: next_command(
            main_window, window, login_entry.get(), password_entry.get()
        ),
    )
    return (
        login_label,
        login_entry,
        label_label,
        password_label,
        password_entry,
        entry_label,
        next_button,
    )


def next_command(
    main_window: CTk.CTk, window: CTk.CTk, login_text: str, password_text: str
):
    print(f'Логин: "{login_text}", Пароль: "{password_text}"')
    destroy(window)
    main_window.mainloop()


def place_widgets(
    widgets: tuple[CTk.CTkEntry | CTk.CTkButton | CTk.CTkLabel],
    padx: float,
    pady: float,
) -> None:
    row_l = 0
    for widget in widgets:
        if type(widget) is tuple:
            widget[0].grid(column=0, row=row_l, padx=padx / 2, pady=pady)
            widget[1].grid(column=1, row=row_l, padx=padx / 2, pady=pady)
        else:
            widget.grid(column=0, columnspan=2, row=row_l, padx=padx, pady=pady)
        row_l += 1


def registration_window(width: int, height: int) -> CTk.CTk:
    win = CTk.CTk()
    win.title("РЕГИСТРАЦИЯ")
    win.configure(fg_color="light gray")
    win.geometry(f"{width}x{height}")
    win.resizable(False, False)
    win.protocol("WM_DELETE_WINDOW", lambda window=win: destroy(window))
    return win


def destroy(window: CTk.CTk):
    window.quit()
    window.destroy()


win = CTk.CTk()
win.protocol("WM_DELETE_WINDOW", lambda window=win: destroy(window))
create_registration_window(
    0,
    {},
    CTk.CTk().winfo_screenwidth() // 7,
    CTk.CTk().winfo_screenheight() // 3,
    win,
)
