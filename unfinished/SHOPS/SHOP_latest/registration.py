import customtkinter as CTk


def create_registration_window(
    len_list_names: int,
    language: dict,
    width: int,
    height: int,
    window: CTk.CTk,
) -> None:
    allow_login = True if len_list_names else False
    allow_login = True

    registration_win = registration_window(width, height)
    registration_win.focus_set()

    if allow_login:
        widgets = create_login_widgets(
            registration_win, width - 20, height - 20, width, height
        )
    else:
        widgets = create_registration_widgets(registration_win, width - 20, height - 20)

    registration_win.mainloop()
    window.mainloop()


def create_registration_widgets(
    window: CTk.CTk,
    widget_width: int,
    widget_height: int,
) -> list | tuple:
    ...


def create_login_widgets(
    window: CTk.CTk,
    widget_width: int,
    widget_height: int,
    frame_width: int,
    frame_height: int,
) -> list | tuple:
    ...


def place_widgets(
    widget_list: list | tuple, pad_x: float | int, pad_y: float | int
) -> None:
    ...


def registration_window(width: int, height: int) -> CTk.CTk:
    win = CTk.CTk()
    win.wm_title("РЕГИСТРАЦИЯ")
    win.configure(fg_color="light gray")
    win.geometry(f"{width}x{height}")
    win.resizable(False, False)
    win.wm_protocol(
        "WM_DELETE_WINDOW", lambda window=win: (window.destroy(), window.quit())
    )
    return win
