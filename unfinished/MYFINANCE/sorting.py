import customtkinter as CTk


def sort_system(self):
    value = self.sorting_button.get()

    if value is None:
        value = "название"

    if len(self.btn_list) > 1:
        if value == "название":
            sorted_list = name_sorting(self, self.btn_list)
        elif value == "дата":
            sorted_list = data_sorting(self, self.btn_list)
        elif value == "время":
            sorted_list = time_sorting(self, self.btn_list)
        elif value == "сумма":
            sorted_list = sum_sorting(self, self.btn_list)
        elif value == "категория":
            sorted_list = category_sorting(self, self.btn_list)
    else:
        sorted_list = self.btn_list

    self.list_frame.destroy()

    # создание рамки списка
    self.list_frame = CTk.CTkScrollableFrame(
        self.win,
        750,
        230,
        fg_color=self.background_widget_color,
        corner_radius=10,
    )
    self.list_frame.place(x=10, y=340)

    # добавление транзакции в список
    self.btn_list = sorted_list

    # создание рамки списка
    self.list_frame = CTk.CTkScrollableFrame(
        self.win,
        750,
        230,
        fg_color=self.background_widget_color,
        corner_radius=10,
    )
    self.list_frame.place(x=10, y=340)

    def save(self, date, name, time, amount, category):
        # создание рамки транзакции
        frame = CTk.CTkFrame(
            self.list_frame, width=734, height=30, fg_color=self.background_widget_color
        )
        frame.pack(padx=10, pady=5)

        # размещение даты в рамке транзакции
        CTk.CTkLabel(
            frame,
            width=200,
            height=30,
            fg_color=self.background_widget_color,
            text=date,
            text_color=self.text_color,
            font=CTk.CTkFont(size=20),
        ).place(x=0, y=0)

        # размещение названия в рамке транзакции
        CTk.CTkLabel(
            frame,
            width=250,
            height=30,
            fg_color=self.background_widget_color,
            text=name,
            text_color=self.text_color,
            font=CTk.CTkFont(size=20),
        ).place(x=200, y=0)

        # размещение времени в рамке транзакции
        CTk.CTkLabel(
            frame,
            width=84,
            height=30,
            fg_color=self.background_widget_color,
            text=time,
            text_color=self.text_color,
            font=CTk.CTkFont(size=20),
        ).place(x=450, y=0)

        # размещение суммы в рамке транзакции
        CTk.CTkLabel(
            frame,
            width=100,
            height=30,
            fg_color=self.background_widget_color,
            text=amount,
            text_color=self.text_color,
            font=CTk.CTkFont(size=20),
        ).place(x=534, y=0)

        # размещение категории в рамке транзакции
        CTk.CTkLabel(
            frame,
            width=100,
            height=30,
            fg_color=self.background_widget_color,
            text=category,
            text_color=self.text_color,
            font=CTk.CTkFont(size=20),
        ).place(x=634, y=0)

    for i in range(len(sorted_list)):
        save(
            self,
            sorted_list[i]["дата"],
            sorted_list[i]["название"],
            sorted_list[i]["время"],
            sorted_list[i]["сумма"],
            sorted_list[i]["категория"],
        )


def name_sorting(self, data_list: list[str]):
    sorted_keys = sorted(data_list[i]["название"] for i in range(len(data_list)))
    sorted_list = []

    for index_key in range(0, len(sorted_keys) - 1, 1):
        if sorted_keys[index_key] == sorted_keys[index_key + 1]:
            data_sorting(self, [data_list[index_key], data_list[index_key + 1]])
        else:
            sorted_list.append(data_list[index_key]["название"])
    sorted_list.append(data_list[-1]["название"])

    return sorted_list


def data_sorting(self, data_list: list[str]):
    sorted_keys = sorted([self.btn_list[i]["дата"] for i in range(len(self.btn_list))])
    sorted_list = []

    for index_key in range(0, len(sorted_keys) - 1, 1):
        if sorted_keys[index_key] == sorted_keys[index_key + 1]:
            time_sorting(self, [data_list[index_key], data_list[index_key + 1]])
        else:
            sorted_list.append(data_list[index_key]["дата"])
    sorted_list.append(data_list[-1]["дата"])

    return sorted_list


def time_sorting(self, data_list: list[str]):
    sorted_keys = sorted([self.btn_list[i]["время"] for i in range(len(self.btn_list))])
    sorted_list = []

    for index_key in range(0, len(sorted_keys) - 1, 1):
        if sorted_keys[index_key] == sorted_keys[index_key + 1]:
            sum_sorting(self, [data_list[index_key], data_list[index_key + 1]])
        else:
            sorted_list.append(data_list[index_key]["время"])
    sorted_list.append(data_list[-1]["время"])

    return sorted_list


def sum_sorting(self, data_list: list[str]):
    sorted_keys = sorted([self.btn_list[i]["сумма"] for i in range(len(self.btn_list))])
    sorted_list = []

    for index_key in range(0, len(sorted_keys) - 1, 1):
        if sorted_keys[index_key] == sorted_keys[index_key + 1]:
            category_sorting(self, [data_list[index_key], data_list[index_key + 1]])
        else:
            sorted_list.append(data_list[index_key]["сумма"])
    sorted_list.append(data_list[-1]["сумма"])

    return sorted_list


def category_sorting(self, data_list: list[str]):
    sorted_keys = sorted(
        [self.btn_list[i]["категория"] for i in range(len(self.btn_list))]
    )
    sorted_list = []

    for index_key in range(0, len(sorted_keys) - 1, 1):
        if sorted_keys[index_key] == sorted_keys[index_key + 1]:
            time_sorting(self, [data_list[index_key], data_list[index_key + 1]])
        else:
            sorted_list.append(data_list[index_key]["категория"])
    sorted_list.append(data_list[-1]["категория"])

    return sorted_list
