def start_solver(board: list, player: str = "X", list_index: bool = False) -> str | int:
    # Противник
    opponent = "O" if player == "X" else "X"

    # Выигрышные комбинации
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

    # Проверка свободности центра поля
    if board[4] not in ["X", "O"]:
        # Возвращаем индекс точки
        return 4 if list_index else 5

    # Проходимся по всем выигрышным комбинациям
    for win in win_combinations:
        # Проверка на свободность первой позиции
        if (
            board[win[1]] == player
            and board[win[2]] == player
            and board[win[0]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[0] if list_index else win[0] + 1

        # Проверка на свободность второй позиции
        if (
            board[win[0]] == player
            and board[win[2]] == player
            and board[win[1]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[1] if list_index else win[1] + 1

        # Проверка на свободность третьей позиции
        if (
            board[win[0]] == player
            and board[win[1]] == player
            and board[win[2]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[2] if list_index else win[2] + 1

    # Предотвращаем выигрыш игрока
    for win in win_combinations:
        # Проверка на свободность первой позиции
        if (
            board[win[1]] == opponent
            and board[win[2]] == opponent
            and board[win[0]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[0] if list_index else win[0] + 1

        # Проверка на свободность второй позиции
        if (
            board[win[0]] == opponent
            and board[win[2]] == opponent
            and board[win[1]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[1] if list_index else win[1] + 1

        # Проверка на свободность третьей позиции
        if (
            board[win[0]] == opponent
            and board[win[1]] == opponent
            and board[win[2]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[2] if list_index else win[2] + 1

    #! БЕЗ ЭТОГО ТОЖЕ ОТЛИЧНО РАБОТАЕТ
    # Проверка на выигрышную комбинацию
    for win in win_combinations:
        # Проверка на свободность первой позиции
        if (
            board[win[0]] == opponent
            and board[win[1]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[1] if list_index else win[1] + 1
        # Проверка на свободность второй позиции
        if (
            board[win[1]] == opponent
            and board[win[0]] not in ["X", "O"]
            and board[win[2]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[0] if list_index else win[0] + 1
        # Проверка на свободность третьей позиции
        if (
            board[win[2]] == opponent
            and board[win[0]] not in ["X", "O"]
            and board[win[1]] not in ["X", "O"]
        ):
            # Возвращаем индекс точки
            return win[0] if list_index else win[0] + 1

    # Проверка на свободность выигрышной комбинации
    for win in win_combinations:
        # Проверка на свободность комбинации
        if (
            board[win[0]] != opponent
            and board[win[1]] != opponent
            and board[win[2]] != opponent
        ):
            # Проверка на свободность 1 позиции
            if board[win[0]] != player:
                # Возвращаем индекс точки
                return win[0] if list_index else win[0] + 1
            # Проверка на свободность 2 позиции
            if board[win[1]] != player:
                # Возвращаем индекс точки
                return win[1] if list_index else win[1] + 1
            # Проверка на свободность 3 позиции
            if board[win[2]] != player:
                # Возвращаем индекс точки
                return win[2] if list_index else win[2] + 1

    # Проверка свободных полей
    for pos in range(0, len(board), 1):
        # Проверка на свободность 1 позиции
        if board[pos] not in ["X", "O"]:
            # Возвращаем индекс точки
            return pos if list_index else pos + 1

    return "Ходов не осталось!"
