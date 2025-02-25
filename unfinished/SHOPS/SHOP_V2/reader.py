# Импорт модулей
from os import listdir
from ujson import load


# Чтение файла конфигурации приложения
def read_config_file(self):
    # Открываем файл конфигураций на чтение
    with open(f"{self.directory}/configure.cfg", "r") as file:
        # Читаем файл без комментариев и преобразуем его в словарь
        result = dict(
            filter(
                None,
                map(
                    lambda txt: txt.replace("\n", "").split(" = ")
                    if txt[0] != "#"
                    else None,
                    file.readlines(),
                ),
            )
        )
    # Возвращаем результат
    return result


# Чтение файла с языковым пакетом
def read_lang_file(self, language: str = "en_US"):
    # Узнаем все имеющиеся файлы с языковыми пакетами
    language_files = set(
        map(
            lambda file: file.split(".")[0] if file.endswith(".txt") else None,
            listdir(f"{self.directory}/languages"),
        )
    )
    # Преобразуем все имеющиеся файлы в список
    language_files = list(filter(None, language_files))

    # Узнаем существует ли выбранный язык в файлах
    language = language if language in language_files else "en_US"

    # Открываем файл языкового пакета на чтение
    with open(f"{self.directory}/languages/{language}.txt", "r") as file:
        # Читаем файл без комментариев и преобразуем его в словарь
        languages = dict(
            filter(
                None,
                map(
                    lambda txt: txt.replace("\n", "").split(" = ")
                    if txt[0] not in ["!", "#", "/", "?"]
                    else None,
                    file.readlines(),
                ),
            )
        )

    # Проходимся по всему словарю
    for key, value in languages.items():
        # Если значение словаря - список
        if value[0] == "[" and value[-1] == "]":
            # Преобразуем строку со списком в список
            value = value.replace("[", "").replace("]", "")
            value = value.split(", ")

        # Если значение словаря - список
        elif value[0] == "{" and value[-1] == "}":
            # Преобразуем строку со словарем в словарь
            value = value.replace("{", "").replace("}", "")
            result = {}
            for val in value.split(", "):
                k, v = val.split(": ")
                result[k] = v
            value = result

        # Записываем итоговое значение ключа в словаре
        languages[key] = value

    # Возвращаем результат
    return languages


# Чтение файла данных приложения
def read_data_files(self):
    # Открываем файл данных на чтение
    with open(f"{self.directory}/data.json", "r") as file:
        # Читаем файл
        data = load(file)
        # Записываем данные в переменные
        self.income = float(data.get("income", 0))
        self.expenditure = float(data.get("expenditure", 0))
        self.shift_number = int(data.get("shift number", 0)) + 1
        self.employs_list_names = data.get("employs names list", [])
        self.employs_name = data.get("employs name", "")
        # Удаляем пустые значение списка
        self.employs_list_names = list(
            filter(
                lambda lst: True
                if type(lst) not in [int, float, bool]
                and bool(lst.replace(" ", "")) is True
                else False,
                self.employs_list_names,
            )
        )
        self.employs_name = (
            self.employs_name.replace(" ", "") if type(self.employs_name) is str else ""
        )

        # Узнаем текущего сотрудника
        if self.employs_list_names == []:
            self.employs_name = ""
        elif (
            len(self.employs_list_names) == 1
            or self.employs_name == self.employs_list_names[-1]
            or self.employs_name == ""
        ):
            self.employs_name = self.employs_list_names[0]
        else:
            res = False
            # Проходимся по списку сотрудников
            for index in self.employs_list_names:
                if res:
                    self.name = index
                    break
                if index == self.name:
                    res = True

        del data

    # Открываем файл списка продуктов на чтение
    with open(f"{self.directory}/products.json", "r") as file:
        # Записываем список продуктов в переменную
        self.products = load(file)
