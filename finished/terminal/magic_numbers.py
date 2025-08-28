from contextlib import suppress
from random import randint


class Main:
    def __init__(self) -> None:
        self.numbers: tuple[int, int] = self.get_user_input_number()
        random_number: int = randint(self.numbers[0], self.numbers[1])
        self.attempts: int = 0
        print(random_number)
        result_attempts: int = self.get_user_magic_number(random_number)
        print(
            f"Вы угадали! Загаданное число было {random_number}. Затраченное количество попыток: {result_attempts}."
        )

    def get_user_input_number(self) -> tuple[int, int]:
        test_number = input(
            'Введите диапазон чисел разделив знаком "-" (пример: 17-63): '
        )
        if len(test_number.split("-")) == 2:
            start_number = test_number.split("-")[0]
            end_number = test_number.split("-")[1]
            if start_number.isdigit() and end_number.isdigit():
                if int(start_number) > 0 and int(end_number) > 0:
                    if int(start_number) > int(end_number):
                        start_number, end_number = end_number, start_number
                    print("Отлично! Число загадано. Игра началась.")
                    return (int(start_number), int(end_number))
                else:
                    print("Числа должны быть больше 0!")

        return self.get_user_input_number()

    def get_user_magic_number(self, random_magic_number: int) -> int:
        self.attempts += 1
        number = input(
            f"Попытка {self.attempts}. Введите число в диапазоне от {self.numbers[0]} до {self.numbers[1]}: "
        )
        if number.isdigit():
            if self.numbers[0] <= int(number) <= self.numbers[1]:
                if int(number) == random_magic_number:
                    return self.attempts
                else:
                    print("Вы не угадали! Попробуйте ещё раз.")
                    return self.get_user_magic_number(random_magic_number)
        self.attempts -= 1
        return self.get_user_magic_number(random_magic_number)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        Main()
