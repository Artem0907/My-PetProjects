from typing import Literal

orange_color, red_color, green_color, reset_color = (
    "\033[33m",
    "\033[31m",
    "\033[32m",
    "\033[0m",
)
board: list[int | Literal["X", "O"]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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


def game_player_step(index: int, player: Literal["X", "O"]) -> bool:
    if 9 < index < 1 or board[index - 1] in ["X", "O"]:
        return False
    board[index - 1] = player
    return True


def game_computer_step() -> int:
    if board[4] not in ["X", "O"]:
        board[4] = "O"
        return 4

    for win in win_combinations:
        if (
            board[win[1]] == "O"
            and board[win[2]] == "O"
            and board[win[0]] not in ["X", "O"]
        ):
            board[win[0]] = "O"
            return win[0]
        if (
            board[win[0]] == "O"
            and board[win[2]] == "O"
            and board[win[1]] not in ["X", "O"]
        ):
            board[win[1]] = "O"
            return win[1]
        if (
            board[win[0]] == "O"
            and board[win[1]] == "O"
            and board[win[2]] not in ["X", "O"]
        ):
            board[win[2]] = "O"
            return win[2]

    for win in win_combinations:
        if (
            board[win[1]] == "X"
            and board[win[2]] == "X"
            and board[win[0]] not in ["X", "O"]
        ):
            board[win[0]] = "O"
            return win[0]
        if (
            board[win[0]] == "X"
            and board[win[2]] == "X"
            and board[win[1]] not in ["X", "O"]
        ):
            board[win[1]] = "O"
            return win[1]
        if (
            board[win[0]] == "X"
            and board[win[1]] == "X"
            and board[win[2]] not in ["X", "O"]
        ):
            board[win[2]] = "O"
            return win[2]

    for win in win_combinations:
        if (
            board[win[0]] == "O"
            and board[win[1]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            board[win[1]] = "O"
            return win[1]
        if (
            board[win[1]] == "O"
            and board[win[0]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            board[win[0]] = "O"
            return win[0]
        if (
            board[win[2]] == "O"
            and board[win[0]] not in ["X", "O"]
            and board[win[1]] not in ["X", "O"]
        ):
            board[win[0]] = "O"
            return win[0]

    for win in win_combinations:
        if board[win[0]] != "X" and board[win[1]] != "X" and board[win[2]] != "X":
            if board[win[0]] != "O":
                board[win[0]] = "O"
                return win[0]
            if board[win[1]] != "O":
                board[win[1]] = "O"
                return win[1]
            if board[win[2]] != "O":
                board[win[2]] = "O"
                return win[2]

    for pos in range(0, len(board), 1):
        if board[pos] not in ["X", "O"]:
            board[pos] = "O"
            return pos


def check_win() -> Literal["X", "O", False]:
    for win_pos in win_combinations:
        if board[win_pos[0]] == board[win_pos[1]] == board[win_pos[2]] and board[
            win_pos[1]
        ] in ["X", "O"]:
            return board[win_pos[1]]  # type: ignore
    return False


def draw_board(new_index: int | None = None, old_index: int | None = None) -> None:
    global board
    new_board = list(map(str, board))
    if old_index:
        new_board[old_index - 1] = red_color + new_board[old_index - 1] + reset_color
    if new_index:
        new_board[new_index - 1] = green_color + new_board[new_index - 1] + reset_color
    for board_index in range(len(new_board)):
        # if new_board[board_index] == "X":
        #     new_board[board_index] = green_color + new_board[board_index] + reset_color
        # if new_board[board_index] == "O":
        #     new_board[board_index] = red_color + new_board[board_index] + reset_color
        if new_board[board_index].isnumeric():
            new_board[board_index] = orange_color + new_board[board_index] + reset_color

    print("    ╷   ╷    ")
    print(f"  {new_board[0]} │ {new_board[1]} │ {new_board[2]}  ")
    print("╶───┼───┼───╴")
    print(f"  {new_board[3]} │ {new_board[4]} │ {new_board[5]}  ")
    print("╶───┼───┼───╴")
    print(f"  {new_board[6]} │ {new_board[7]} │ {new_board[8]}  ")
    print("    ╵   ╵    ")


def start_player_game() -> None:
    step: int = 1
    current_player: str = "X"

    while step < 10 and check_win() == False:
        try:
            index: int = int(
                input(
                    f"\nХодит игрок {current_player}. Введите номер поля (0 - выход): "
                )[0]
            )
        except:
            draw_board()
            print("Повторите ход!")
            continue

        if index == 0:
            break

        if game_player_step(index, current_player):
            current_player: str = "X" if current_player == "O" else "O"
            step += 1
            draw_board()
            print("Удачный ход!")
        else:
            draw_board()
            print("Повторите ход!")

    if index == 0:
        print("\nВы вышли из игры!")
    elif check_win():
        print("\nВыиграл игрок:", check_win())
    else:
        print("\nНичья!")


def start_computer_game() -> None:
    step: int = 1

    while step < 10 and check_win() == False:
        try:
            index: int = int(
                input(f"\nХодит игрок. Введите номер поля (0 - выход): ")[0]
            )
        except:
            draw_board()
            print("Повторите ход!")
            continue

        if index == 0:
            break

        if game_player_step(index, "X"):
            step += 1
            if check_win():
                draw_board()
                print("Удачный ход!")
                break

            step += 1
            game_computer_step()
            draw_board()
            print("Удачный ход!")
        else:
            draw_board()
            print("Повторите ход!")
            continue

    if index == 0:
        print("\nВы вышли из игры!")
    elif check_win() == "O":
        print("\nВы проиграли!")
    elif check_win() == "X":
        print("\nВы выиграли!")
    else:
        print("\nНичья!")


def start_game() -> None:
    print("Добро пожаловать в игру крестики-нолики!")

    while True:
        mode = input(
            "\nВыберите режим игры\n0 - выход\n1 - игрок против игрока\n2 - игрок против компьютера\n\nВаш выбор: "
        )
        match mode:
            case "0":
                print("До скорых встреч!")
                break
            case "1":
                draw_board()
                start_player_game()
            case "2":
                draw_board()
                start_computer_game()
            case _:
                print("Неправильно введён режим игры! Попробуйте ещё раз!")
                continue


if __name__ == "__main__":
    start_game()
