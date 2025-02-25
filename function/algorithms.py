def sort_json(json_data):
    if isinstance(json_data, (set, tuple, list)):
        try:
            json_data = sorted(json_data)
        except TypeError:
            json_data = list(json_data)
        for json_id, json_obj in enumerate(json_data):
            json_data[json_id] = sort_json(json_obj)
    elif isinstance(json_data, dict):
        json_data = dict(sorted(json_data.items()))
        for json_key, json_value in json_data.items():
            json_data[json_key] = sort_json(json_value)
    return json_data


def center(
    x0: int | float, y0: int | float, x: int | float, y: int | float
) -> tuple[float, float]:
    return ((max(x0, x) - min(x0, x)) / 2, (max(y0, y) - min(y0, y)) / 2)


def num_to_words(number: int):
    global value
    if number == 0:
        return "нуль"
    value = number
    UNITS = 0
    TENS = 1
    HUNDREDS = 2
    AMOUNT_BLOCKS = 4
    units = [
        "один",
        "два",
        "три",
        "четыре",
        "пять",
        "шесть",
        "семь",
        "восемь",
        "девять",
    ]
    units2 = [
        "одна",
        "две",
        "три",
        "четыре",
        "пять",
        "шесть",
        "семь",
        "восемь",
        "девять",
    ]
    units_after_ten = [
        "одиннадцать",
        "двенадцать",
        "тринадцать",
        "четырнадцать",
        "пятнадцать",
        "шестнадцать",
        "семнадцать",
        "восемнадцать",
        "девятнадцать",
    ]
    tens = [
        "десять",
        "двадцать",
        "тридцать",
        "сорок",
        "пятьдесят",
        "шестьдесят",
        "семьдесят",
        "восемьдесят",
        "девяносто",
    ]
    hundreds = [
        "сто",
        "двести",
        "триста",
        "четыреста",
        "пятьсот",
        "шестьсот",
        "семьсот",
        "восемьсот",
        "девятьсот",
    ]
    rubles = ["рубль", "рубля", "рублей"]
    thousands = ["тысяча", "тысячи", "тысяч"]
    millions = ["миллион", "миллиона", "миллионов"]
    billions = ["биллион", "биллиона", "биллионов"]

    result = ""
    current_block = 0

    def fix_result(result):
        if result.find("рубл") == 0:
            return f"{result} рублей"
        return result

    def mas(e):
        global value
        result = value % 10
        value = value // 10
        return result

    while current_block < AMOUNT_BLOCKS and value > 0:
        unit_case = [units, units2, units, units][current_block]
        block_end = [rubles, thousands, millions, billions][current_block]

        unit, ten, hundred = map(mas, [UNITS, TENS, HUNDREDS])
        if unit == 1 and ten != 1:
            result = f"{unit_case[unit-1]} {block_end[0]} {result}"
        elif unit >= 2 and unit <= 4 and ten != 1:
            result = f"{unit_case[unit-1]} {block_end[1]} {result}"
        elif unit > 4 and ten != 1:
            result = f"{unit_case[unit-1]} {block_end[2]} {result}"

        if ten == 1 and unit != 0:
            result = f"{units_after_ten[unit-1]} {block_end[2]} {result}"
        elif ten == 1 and unit == 0:
            result = f"{tens[ten -1]} {block_end[2]} {result}"
        elif ten > 1 and unit != 0:
            result = f"{tens[ten -1]} {result}"
        # else:
        #     result = f"{tens[unit-1]} {block_end[2]}"

        if hundred > 0 and unit + ten == 0:
            result = f"{hundreds[hundred - 1]} {block_end[2]} {result}"
        elif hundred > 0 and unit + ten != 0:
            result = f"{hundreds[hundred - 1]} {result}"

        current_block += 1

    result = fix_result(result)
    return result


def plus_one(digits: list[int]) -> list[int]:
    for i in range(len(digits) - 1, -1, -1):
        if str(digits[i]) == 9:
            digits[i] = 0
        else:
            digits[i] = digits[i] + 1
            return digits

    digits.append(0)
    digits[0] = 1

    return digits


def select(num: int, nominative: str, accusatory: str, genitive: str) -> str | None:
    if not isinstance(num, int):
        return None

    if num % 10 > 4 or num % 10 == 0:
        return f"{num} {genitive}"
    elif num % 10 == 1:
        return f"{num} {nominative}"
    else:
        return f"{num} {accusatory}"


def selection_sort(array: list[int]) -> list[int]:
    for i in range(len(array)):
        min = array[i]
        min_id = i
        for j in range(i, len(array)):
            if array[j] < min:
                min = array[j]
                min_id = j
        temp = array[i]
        array[i] = min
        array[min_id] = temp
    return array
