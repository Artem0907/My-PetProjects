from typing import Literal
from random import shuffle


orange_color, red_color, green_color, reset_color = (
    "\033[33m",
    "\033[31m",
    "\033[32m",
    "\033[0m",
)

win_combinations = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]
shuffle(win_combinations)


def player_step(index: int, player: Literal["X", "O"], board: list) -> bool:
    if 0 < index < 10 and player in ["X", "O"] and board[index - 1] not in ["X", "O"]:
        return True
    return False


def computer_step(board: list) -> int:  # type: ignore
    if board[4] not in ["X", "O"]:
        return 4

    for win in win_combinations:
        if (
            board[win[1]] == "O"
            and board[win[2]] == "O"
            and board[win[0]] not in ["X", "O"]
        ):
            return win[0]
        if (
            board[win[0]] == "O"
            and board[win[2]] == "O"
            and board[win[1]] not in ["X", "O"]
        ):
            return win[1]
        if (
            board[win[0]] == "O"
            and board[win[1]] == "O"
            and board[win[2]] not in ["X", "O"]
        ):
            return win[2]

    for win in win_combinations:
        if (
            board[win[1]] == "X"
            and board[win[2]] == "X"
            and board[win[0]] not in ["X", "O"]
        ):
            return win[0]
        if (
            board[win[0]] == "X"
            and board[win[2]] == "X"
            and board[win[1]] not in ["X", "O"]
        ):
            return win[1]
        if (
            board[win[0]] == "X"
            and board[win[1]] == "X"
            and board[win[2]] not in ["X", "O"]
        ):
            return win[2]

    for win in win_combinations:
        if (
            board[win[0]] == "O"
            and board[win[1]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            return win[1]
        if (
            board[win[1]] == "O"
            and board[win[0]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            return win[0]
        if (
            board[win[2]] == "O"
            and board[win[1]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            return win[1]

    for pos in range(len(board)):
        if board[pos] not in ["X", "O"]:
            return pos


def check_win(win_pos: list, board: list) -> Literal["X", "O", False]:
    for win in win_pos:
        if board[win[0]] == board[win[1]] == board[win[2]] and board[win[1]] in [
            "X",
            "O",
        ]:
            return board[win[1]]
    return False


def draw_board(
    board: list, new_index: int | None = None, old_index: int | None = None
) -> None:
    board = list(map(str, board))

    if old_index:
        board[old_index - 1] = red_color + board[old_index - 1] + reset_color
    if new_index:
        board[new_index - 1] = green_color + board[new_index - 1] + reset_color
    for board_index in range(len(board)):
        if board[board_index].isnumeric():
            board[board_index] = orange_color + board[board_index] + reset_color

    print("    ╷   ╷    ")
    print(f"  {board[0]} │ {board[1]} │ {board[2]}  ")
    print("╶───┼───┼───╴")
    print(f"  {board[3]} │ {board[4]} │ {board[5]}  ")
    print("╶───┼───┼───╴")
    print(f"  {board[6]} │ {board[7]} │ {board[8]}  ")
    print("    ╵   ╵    ")


def start_player_game(win_pos: list, board: list) -> None:
    step = 1
    current_player: Literal["X", "O"] = "X"
    index = old_index = None

    while step < 10 and not check_win(win_pos, board):
        try:
            old_index = index
            index = int(
                input(
                    f"\nХодит игрок {current_player}. Введите номер поля (0 - выход): "
                )[0]
            )
        except ValueError:
            draw_board(board, index, old_index)
            print("Повторите ход!")
            continue

        if index == 0:
            break

        if player_step(index, current_player, board):
            board[index - 1] = current_player
            current_player = "X" if current_player == "O" else "O"
            step += 1
            draw_board(board, index, old_index)
            print("Удачный ход!")
        else:
            index = old_index
            old_index = None
            draw_board(board, index, old_index)
            print("Повторите ход!")

    draw_board(board, old_index)
    if index == 0:
        print("\nВы вышли из игры!")
    elif check_win(win_pos, board):
        print("\nВыиграл игрок:", check_win(win_pos, board))
    else:
        print("\nНичья!")


def start_computer_game(win_pos: list, board: list) -> None:
    step = 1
    index = old_index = None

    while step < 10 and not check_win(win_pos, board):
        try:
            old_index = index
            index = int(input(f"\nХодит игрок. Введите номер поля (0 - выход): "))
        except ValueError:
            draw_board(board, index, old_index)
            print("Повторите ход!")
            continue

        if index == 0:
            break

        if player_step(index, "X", board):
            board[index - 1] = "X"
            step += 1
            if check_win(win_pos, board):
                draw_board(board, index, old_index)
                print("Удачный ход!")
                break

            step += 1
            old_index = index
            index = computer_step(board)
            if index == None:
                break
            board[index] = "O"
            draw_board(board, index + 1, old_index)
            print("Удачный ход!")
        else:
            index = old_index
            old_index = None
            draw_board(board, index, old_index)
            print("Повторите ход!")
            continue

    draw_board(board, old_index)
    if index == 0:
        print("\nВы вышли из игры!")
    elif check_win(win_pos, board) == "O":
        print("\nВы проиграли!")
    elif check_win(win_pos, board) == "X":
        print("\nВы выиграли!")
    else:
        print("\nНичья!")


if __name__ == "__main__":
    print("Добро пожаловать в игру крестики-нолики!")

    while True:
        board: list[int | Literal["X", "O"]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        mode = input(
            "\nВыберите режим игры\n0 - выход\n1 - игрок против игрока\n2 - игрок против компьютера\n\nВаш выбор: "
        )
        match mode:
            case "0":
                print("До скорых встреч!")
                break
            case "1":
                draw_board(board)
                start_player_game(win_combinations, board)
            case "2":
                draw_board(board)
                start_computer_game(win_combinations, board)
