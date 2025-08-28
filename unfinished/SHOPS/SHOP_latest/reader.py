from os import listdir
from ujson import dump, load
from json.decoder import JSONDecodeError


def read_configure(directory: str) -> dict:
    with open(f"{directory}/configure.ini", "r", encoding="utf-8") as file:
        configures = list(
            map(lambda txt: txt.replace("\n", "").lower(), file.readlines())
        )

        result = {}
        temp = ""
        lst = {}
        for configure in configures:
            if len(configure) != 0 and configure[0] not in [";", "#"]:
                if configure[0] == "[" and configure[-1] == "]":
                    result[temp] = lst
                    lst = {}
                    temp = configure[1:-1]
                else:
                    configure = list(map(lambda txt: txt.strip(), configure.split("=")))
                    lst[configure[0]] = configure[1]

            result[temp] = lst
        del result[""]
        return result


def read_language(directory: str, lang: str = "en_US") -> dict:
    language_files = set(
        map(
            lambda file: file.split(".")[0] if file.endswith(".txt") else None,
            listdir(f"{directory}/languages"),
        )
    )
    language_files = list(filter(None, language_files))

    lang = lang if lang in language_files else "en_US"

    with open(f"{directory}/languages/{lang}.txt", "r", encoding="utf-8") as file:
        languages = list(
            map(lambda txt: txt.replace("\n", "").lower(), file.readlines())
        )

        result = {}
        temp = ""
        lst = []
        for language in languages:
            if len(language) != 0:
                if language[0:2] == "#_" and language[-2:] == "_#":
                    result[temp] = "\n".join(lst)
                    lst = []
                    temp = language[2:-2]
                else:
                    lst.append(language)

            result[temp] = "\n".join(lst)
        result[""] = ""
        del result[""]

        return result


def read_data(directory: str) -> tuple:
    with open(f"{directory}/json/data.json", "r", encoding="utf-8") as file:
        data = load(file)

        income = float(data.get("income", 0))
        expenditure = float(data.get("expenditure", 0))
        shift_number = int(data.get("shift number", 0)) + 1
        employs_list_names = data.get("employs names list", [])
        employs_name = data.get("employs name", "")

        employs_list_names = list(
            filter(
                lambda lst: True
                if type(lst) is str and bool(str(lst).replace(" ", "")) is True
                else False,
                employs_list_names,
            )
        )
        employs_name = (
            employs_name.replace(" ", "") if type(employs_name) is str else ""
        )
        return (income, expenditure, shift_number, employs_list_names, employs_name)


def read_favorites(directory: str) -> dict:
    with open(f"{directory}/json/favorites.json", "r", encoding="utf-8") as file:
        return load(file)


def read_product_list(directory: str) -> list:
    with open(f"{directory}/json/products.json", "r", encoding="utf-8") as file:
        return load(file)


def file_except(directory: str, file_type: type, read_file: str) -> None:
    try:
        with open(f"{directory}/{read_file}", "r", encoding="utf-8") as file:
            if type(load(file)) != file_type:
                raise FileNotFoundError
    except FileNotFoundError:
        with open(f"{directory}/{read_file}", "w", encoding="utf-8") as file:
            dump({}, file, ensure_ascii=False)
    except JSONDecodeError:
        with open(f"{directory}/{read_file}", "w", encoding="utf-8") as file:
            dump({}, file, ensure_ascii=False)


def read_files(directory: str) -> tuple:
    file_except(directory, dict, "json/data.json")
    file_except(directory, dict, "json/favorites.json")
    file_except(directory, list, "json/products.json")

    return (
        read_configure(directory),
        read_data(directory),
        read_favorites(directory),
        read_product_list(directory),
    )
