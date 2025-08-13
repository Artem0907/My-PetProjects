from typing import Callable, Literal
from customtkinter import CTk, CTkButton
from logging import (
    NOTSET,
    DEBUG,
    INFO,
    StreamHandler,
    basicConfig,
    getLogger,
)

basicConfig(
    format="[{asctime}] {levelname} | {message}",
    datefmt="%d/%m/%Y %H:%M:%S",
    style="{",
    level=NOTSET,
    encoding="utf-8",
    handlers=[StreamHandler()],
)
logger = getLogger("tic-tac-toe")


_WIN_COMBINATIONS: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)
type board_type = list[int | Literal["X", "O"]]
logger.log(DEBUG, "win combinations is created success")


class Game:
    def __init__(self, user: Literal["X", "O"] = "X"):
        self.board: list[int | Literal["X", "O"]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.step = 0

        self.user: Literal["X", "O"] = user
        self.computer: Literal["X", "O"] = "O" if user == "X" else "X"
        logger.log(
            INFO, "game started as user[%s] and computer[%s]", self.user, self.computer
        )
        self.window = CTk("white")
        self.window.title("TIC-TAC-TOE")
        logger.log(DEBUG, "window init")

        screen_geometry = (
            self.window.winfo_screenwidth() + self.window.winfo_screenheight()
        ) // 8
        self.window.geometry(f"{screen_geometry}x{screen_geometry}")

        self.buttons: list[CTkButton] = self.create_widgets(
            self.window, screen_geometry // 3, "white", "green", self.click_button
        )
        logger.log(INFO, "buttons created")

    def __call__(self):
        logger.log(DEBUG, "window stated mainloop")
        self.window.mainloop()

    def computer_step(
        self, board: board_type, buttons: list[CTkButton], fore_color: str
    ) -> None:
        logger.log(DEBUG, "start computer step")
        if board[4] not in ["X", "O"]:
            buttons[4].configure(
                text=self.computer, state="disabled", fg_color=fore_color
            )
            board[4] = self.computer
            logger.log(DEBUG, "computer 4 (center)")
            return

        for position in _WIN_COMBINATIONS:
            for positions_id in [(0, 1, 2), (1, 2, 0), (0, 2, 1)]:
                if (
                    board[position[positions_id[0]]] == self.computer
                    and board[position[positions_id[1]]] == self.computer
                    and board[position[positions_id[2]]] != self.user
                ):
                    buttons[position[positions_id[2]]].configure(
                        text=self.computer, state="disabled", fg_color=fore_color
                    )
                    board[position[positions_id[2]]] = self.computer
                    logger.log(
                        DEBUG, "computer win combination (%s %s %s)", *positions_id
                    )
                    return

        for position in _WIN_COMBINATIONS:
            for positions_id in [(0, 1, 2), (1, 2, 0), (0, 2, 1)]:
                if (
                    board[position[positions_id[0]]] == self.user
                    and board[position[positions_id[1]]] == self.user
                    and board[position[positions_id[2]]] != self.computer
                ):
                    buttons[position[positions_id[2]]].configure(
                        text=self.computer, state="disabled", fg_color=fore_color
                    )
                    board[position[positions_id[2]]] = self.computer
                    logger.log(DEBUG, "computer user block (%s %s %s)", *positions_id)
                    return

        for position in _WIN_COMBINATIONS:
            if (
                board[position[0]] not in ["X", "O"]
                and board[position[1]] not in ["X", "O"]
                and board[position[2]] not in ["X", "O"]
            ):
                buttons[position[1]].configure(
                    text=self.computer, state="disabled", fg_color=fore_color
                )
                board[position[1]] = self.computer
                logger.log(DEBUG, "computer random step (%s %s %s)", *position)
                return

            if board[position[0]] not in ["X", "O"]:
                buttons[position[0]].configure(
                    text=self.computer, state="disabled", fg_color=fore_color
                )
                board[position[0]] = self.computer
                logger.log(DEBUG, "computer random step #1 (%s %s %s)", *position)
                return

            if board[position[1]] not in ["X", "O"]:
                buttons[position[1]].configure(
                    text=self.computer, state="disabled", fg_color=fore_color
                )
                board[position[1]] = self.computer
                logger.log(DEBUG, "computer random step #2 (%s %s %s)", *position)
                return

            if board[position[2]] not in ["X", "O"]:
                buttons[position[2]].configure(
                    text=self.computer, state="disabled", fg_color=fore_color
                )
                board[position[2]] = self.computer
                logger.log(DEBUG, "computer random step #3 (%s %s %s)", *position)
                return

    def create_widgets(
        self,
        window: CTk,
        geometry: int,
        text_color: str,
        button_color: str,
        func: Callable[[board_type, CTkButton, int], None],
    ) -> list[CTkButton]:
        buttons = [
            CTkButton(
                master=window,
                width=geometry,
                height=geometry,
                corner_radius=0,
                text=str(num),
                text_color=text_color,
                fg_color=button_color,
                hover_color=f"dark {button_color}",
            )
            for num in range(1, 10, 1)
        ]
        logger.log(DEBUG, "ctk butttons is created")
        for button_id, button in enumerate(buttons):
            button.configure(
                command=lambda button_=button, button_id_=button_id: func(
                    self.board, button_, button_id_
                )
            )
            button.place(x=(button_id % 3) * geometry, y=(button_id // 3) * geometry)
            logger.log(DEBUG, "ctk button place #%s", button_id + 1)
        logger.log(DEBUG, "ctk buttons placeв success")
        return buttons

    def click_button(
        self, board: board_type, button: CTkButton, button_id: int
    ) -> None:
        board[button_id] = self.user
        button.configure(text=self.user, state="disabled", fg_color="blue")
        logger.log(INFO, "user clicked %s", button_id + 1)
        self.step += 1
        if self.print_winner(board):
            return
        self.computer_step(board, self.buttons, "red")
        logger.log(INFO, "computer clicked %s", button_id + 1)
        self.step += 1
        self.print_winner(board)

    def check_win(self, board: board_type) -> Literal["X", "O", False]:
        for position in _WIN_COMBINATIONS:
            if board[position[0]] == board[position[1]] == board[position[2]]:
                board_pos: Literal["X", "O"] | int = board[position[1]]
                if board_pos in ["X", "O"]:
                    logger.log(
                        INFO, "win is %s in pos (%s %s %s)", board_pos, *position
                    )
                    return board_pos  # type: ignore
        return False

    def print_board(self) -> None:
        print(self.board[0], self.board[1], self.board[2])
        print(self.board[3], self.board[4], self.board[5])
        print(self.board[6], self.board[7], self.board[8])
        logger.log(INFO, "board printed success")

    def print_winner(self, board: board_type) -> bool:
        win: Literal["X", "O", False] = self.check_win(board)
        if win:
            winner = "user" if win == self.user else "computer"
            logger.log(DEBUG, "winner %s (%s)", win)
            print(f"Выиграл: {win}[{winner}]")
            self.print_board()
            self.window.destroy()
            return True
        if self.step == 9:
            logger.log(DEBUG, "drawing")
            print("Ничья")
            self.print_board()
            self.window.destroy()
            return True
        return False


if __name__ == "__main__":
    game = Game("X")
    game()
