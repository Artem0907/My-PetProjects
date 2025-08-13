from typing import Literal
import customtkinter as CTk


class Game:
    win_combinations: list[tuple[int, int, int]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    step = 1

    def __init__(self, user: Literal["X", "O"]):
        self.board: list[int | Literal["X", "O"]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.user: Literal["X", "O"] = user
        self.computer: Literal["X", "O"] = "X" if user == "O" else "O"
        self.win = CTk.CTk()
        self.geometry = (
            self.win.winfo_screenwidth() + self.win.winfo_screenheight()
        ) // 8
        self.create_window(self.win, "TIC-TAC-TOE", self.geometry)
        self.buttons = self.create_widgets(
            self.win, self.geometry // 3, "white", "green", self.button_click
        )

    def __call__(self):
        self.win.mainloop()

    def create_window(self, win: CTk.CTk, win_title: str, geometry: int):
        win.geometry(f"{geometry}x{geometry}+{geometry//3}+{geometry//3}")
        win.title(win_title)
        win.resizable(False, False)

    def create_widgets(
        self, win: CTk.CTk, geometry: int, text_color: str, button_color: str, func
    ):
        buttons = [
            CTk.CTkButton(
                master=win,
                width=geometry,
                height=geometry,
                corner_radius=0,
                text=f"{num}",
                text_color=text_color,
                fg_color=button_color,
                hover_color=f"dark {button_color}",
            )
            for num in range(1, 10, 1)
        ]
        for button_id, button in enumerate(buttons):
            button.configure(command=func(button, button_id))
            button.place(x=(button_id % 3) * geometry, y=(button_id // 3) * geometry)
        return buttons

    def button_click(self, button, button_id):
        def wrapper(button, button_id):
            self.board[button_id] = self.user
            button.configure(text=self.user, state="disabled", fg_color="blue")
            self.step += 1

            if self.check_win(self.board):
                print("Выиграл:", self.check_win(self.board))
                self.turbo_print()
                self.win.destroy()
                return

            if self.step == 11:
                print("Ничья")
                self.turbo_print()
                self.win.destroy()
                return

            self.computer_step(self.board, self.buttons)
            self.step += 1

            if self.check_win(self.board):
                print("Выиграл:", self.check_win(self.board))
                self.turbo_print()
                self.win.destroy()
                return

            if self.step == 11:
                print("Ничья")
                self.turbo_print()
                self.win.destroy()
                return

        return lambda: wrapper(button, button_id)

    def check_win(self, board: list[int | Literal["X", "O"]]):
        for position in self.win_combinations:
            if board[position[0]] == board[position[1]] == board[position[2]]:
                if board[position[0]] in ["X", "O"]:
                    return board[position[0]]
        return False

    def computer_step(
        self, board: list[int | Literal["X", "O"]], buttons: list[CTk.CTkButton]
    ):
        if board[4] not in ["X", "O"]:
            buttons[4].configure(text=self.computer, state="disabled", fg_color="red")
            board[4] = self.computer
            return

        for position in self.win_combinations:
            if (
                board[position[0]] == self.computer
                and board[position[1]] == self.computer
                and board[position[2]] != self.user
            ):
                buttons[position[2]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[2]] = self.computer
                return

            if (
                board[position[1]] == self.computer
                and board[position[2]] == self.computer
                and board[position[0]] != self.user
            ):
                buttons[position[0]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[0]] = self.computer
                return

            if (
                board[position[0]] == self.computer
                and board[position[2]] == self.computer
                and board[position[1]] != self.user
            ):
                buttons[position[1]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[1]] = self.computer
                return

        for position in self.win_combinations:
            if (
                board[position[0]] == self.user
                and board[position[1]] == self.user
                and board[position[2]] != self.computer
            ):
                buttons[position[2]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[2]] = self.computer
                return

            if (
                board[position[1]] == self.user
                and board[position[2]] == self.user
                and board[position[0]] != self.computer
            ):
                buttons[position[0]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[0]] = self.computer
                return

            if (
                board[position[0]] == self.user
                and board[position[2]] == self.user
                and board[position[1]] != self.computer
            ):
                buttons[position[1]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[1]] = self.computer
                return

        for position in self.win_combinations:
            if (
                board[position[0]] not in ["X", "O"]
                and board[position[1]] not in ["X", "O"]
                and board[position[2]] not in ["X", "O"]
            ):
                buttons[position[0]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[0]] = self.computer
                return

            if board[position[0]] not in ["X", "O"]:
                buttons[position[0]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[0]] = self.computer
                return

            if board[position[1]] not in ["X", "O"]:
                buttons[position[1]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[1]] = self.computer
                return

            if board[position[2]] not in ["X", "O"]:
                buttons[position[2]].configure(
                    text=self.computer, state="disabled", fg_color="red"
                )
                board[position[2]] = self.computer
                return

    def turbo_print(self):
        print(self.board[0], self.board[1], self.board[2])
        print(self.board[3], self.board[4], self.board[5])
        print(self.board[6], self.board[7], self.board[8])


game = Game("X")
game()
