import logging
from typing import Any, Union


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sort_json(data: Any) -> Any:
    """
    Recursively sorts JSON-like data structures including:
    - Lists/Tuples/Sets: Attempt to sort elements, maintain original type
    - Dictionaries: Sort by keys, recursively sort values
    - Scalars: Return as-is

    Preserves:
    - Tuple → Tuple
    - Set → List (sorted)
    - List → List (sorted)
    - Dict → Dict (sorted by keys)
    """

    if isinstance(data, dict):
        return {
            key: sort_json(value)
            for key, value in sorted(data.items(), key=lambda x: str(x[0]))
        }

    if isinstance(data, (set, list, tuple)):
        try:
            sorted_data = sorted(data, key=_safe_sort_key)
        except TypeError:
            sorted_data = list(data)

        processed = [sort_json(item) for item in sorted_data]

        # Preserve original container type
        if isinstance(data, tuple):
            return tuple(processed)
        if isinstance(data, set):
            return processed  # Set becomes sorted list
        return processed

    return data


def _safe_sort_key(item: Any) -> Union[Any, str]:
    """Sort key with fallback for unhashable types"""
    try:
        return (str(type(item)), item)
    except TypeError:
        return str(item)


def center(
    x0: int | float, y0: int | float, x: int | float, y: int | float
) -> tuple[float, float]:
    return ((max(x0, x) - min(x0, x)) / 2, (max(y0, y) - min(y0, y)) / 2)


# Константы для числительных
_UNITS = ["один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
_UNITS_FEMININE = [
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
_UNITS_AFTER_TEN = [
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
_TENS = [
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
_HUNDREDS = [
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

# Блоки числительных с их окончаниями
_CURRENCY_BLOCKS = [
    (["миллиард", "миллиарда", "миллиардов"], False),
    (["миллион", "миллиона", "миллионов"], False),
    (["тысяча", "тысячи", "тысяч"], True),
    (["рубль", "рубля", "рублей"], False),
]


def num_to_words(number: int) -> str:
    """
    Конвертирует целое число в его текстовое представление на русском языке с указанием валюты.

    Args:
        number (int): Число для конвертации (0 <= number <= 10^12-1)

    Returns:
        str: Текстовое представление числа с валютой

    Примеры:
        >>> num_to_words(1_234_567)
        'один миллион двести тридцать четыре тысячи пятьсот шестьдесят семь рублей'
        >>> num_to_words(76_534)
        'семьдесят шесть тысяч пятьсот тридцать четыре рубля'
    """
    if number < 0:
        raise ValueError("Отрицательные числа не поддерживаются")
    if number == 0:
        return "ноль рублей"

    def get_block_words(n: int, is_feminine: bool) -> list[str]:
        """Возвращает текстовое представление блока из трех цифр."""
        words = []
        hundreds = n // 100
        tens_units = n % 100

        if hundreds > 0:
            words.append(_HUNDREDS[hundreds - 1])

        if 11 <= tens_units <= 19:
            words.append(_UNITS_AFTER_TEN[tens_units - 11])
        else:
            tens = tens_units // 10
            units = tens_units % 10
            if tens > 0:
                words.append(_TENS[tens - 1])
            if units > 0:
                words.append(
                    _UNITS_FEMININE[units - 1] if is_feminine else _UNITS[units - 1]
                )

        return words

    def get_ending(n: int, endings: list[str]) -> str:
        """Возвращает правильное окончание для блока."""
        if 11 <= n % 100 <= 19:
            return endings[2]
        last_digit = n % 10
        if last_digit == 1:
            return endings[0]
        if 2 <= last_digit <= 4:
            return endings[1]
        return endings[2]

    result: list[str] = []
    remaining = number

    # Обрабатываем блоки от старших к младшим
    for endings, is_feminine in _CURRENCY_BLOCKS:
        if remaining == 0:
            continue

        block_value = remaining % 1000
        remaining = remaining // 1000

        if block_value == 0:
            continue

        block_words = get_block_words(block_value, is_feminine)
        ending = get_ending(block_value, endings)
        block_words.append(ending)
        result = block_words + result

    # Если результат пуст, добавляем "рублей"
    if not result:
        result.append("рублей")

    return " ".join(result).replace("  ", " ").strip()


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
