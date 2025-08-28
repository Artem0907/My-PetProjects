# Импорт библиотек и файлов
import customtkinter as CTk


# добавление данных в списке продуктов
def create_check_box(self, name: str) -> None:
    # какой продукт нужно добавить в список
    if name == self.products[0][0]:
        # добавляем к сумме цену продукта
        self.total_price.configure(
            text=str(
                str(self.total_price.cget("text").split(": ")[0])
                + ": "
                + str(
                    round(
                        float(self.total_price.cget("text").split(": ")[1])
                        + self.products[0][1],
                        2,
                    )
                )
            )
        )

        # добавляем к сумме с процентами цену продукта
        self.total_percent_price.configure(
            text=(
                str(self.total_percent_price.cget("text").split(": ")[0])
                + ": "
                + str(
                    round(
                        (
                            float(self.total_price.cget("text").split(": ")[1])
                            - float(
                                (
                                    (
                                        float(
                                            self.total_price.cget("text").split(": ")[1]
                                        )
                                    )
                                    / 100
                                )
                                * float(
                                    self.total_percent.cget("text")
                                    .split(": ")[1]
                                    .replace("%", "")
                                )
                            )
                        ),
                        2,
                    )
                )
            )
        )

        # добавляем к сумме вес продукта
        self.total_weight.configure(
            text=str(
                str(self.total_weight.cget("text").split(": ")[0])
                + ": "
                + str(
                    int(
                        float(self.total_weight.cget("text").split(": ")[1])
                        + self.products[0][2]
                    )
                )
            )
        )

        # наличие продукта в списке
        if self.products[0][0] in self.check_box_list:
            # изменяем цену за весь продукт и его количество
            self.check_box_list[self.products[0][0]] += 1
            self.amount1.configure(text=self.check_box_list[self.products[0][0]])
            self.sum1.configure(
                text=round(
                    self.products[0][1] * int(self.amount1.cget("text")),
                    2,
                )
            )
            self.weight1.configure(
                text=self.products[0][2] * int(self.amount1.cget("text"))
            )
        else:
            # создание и размещение главной рамки продукта в списке
            self.products_label1 = CTk.CTkLabel(
                self.price_data_label,
                width=self.price_data_list_width * 14.5,
                height=self.price_data_list_height,
                bg_color=self.background_list_color,
                text="",
                corner_radius=0,
            )
            self.products_label1.grid()

            # создание и размещение номера продукта в списке
            self.number1 = CTk.CTkLabel(
                self.price_number_label,
                width=self.price_number_label.cget("width"),
                height=self.price_data_list_height,
                text=self.number_price_label,
                text_color=self.text_color,
            )
            self.number1.grid()

            # создание и размещение названия продукта в списке
            self.name1 = CTk.CTkLabel(
                self.products_label1,
                width=self.price_data_list_width * 4,
                height=self.price_data_list_height,
                text=name,
                text_color=self.text_color,
            )
            self.name1.place(x=0, y=0)

            # создание и размещение количества продукта в списке
            self.amount1 = CTk.CTkLabel(
                self.products_label1,
                width=self.price_data_list_width * 2,
                height=self.price_data_list_height,
                text="1",
                text_color=self.text_color,
            )
            self.amount1.place(x=self.price_data_list_width * 4, y=0)

            # создание и размещение веса продукта в списке
            self.weight1 = CTk.CTkLabel(
                self.products_label1,
                width=self.price_data_list_width * 3,
                height=self.price_data_list_height,
                text=self.products[0][2],
                text_color=self.text_color,
            )
            self.weight1.place(x=self.price_data_list_width * 6, y=0)

            # создание и размещение цены продукта в списке
            self.price1 = CTk.CTkLabel(
                self.products_label1,
                width=self.price_data_list_width * 2,
                height=self.price_data_list_height,
                text=self.products[0][1],
                text_color=self.text_color,
            )
            self.price1.place(x=self.price_data_list_width * 9, y=0)

            # создание и размещение суммы продукта в списке
            self.sum1 = CTk.CTkLabel(
                self.products_label1,
                width=self.price_data_list_width * 2,
                height=self.price_data_list_height,
                text=self.products[0][1],
                text_color=self.text_color,
            )
            self.sum1.place(x=self.price_data_list_width * 11, y=0)

            # создание и размещение кнопки удаления продукта из списка
            self.check1 = CTk.CTkButton(
                self.products_label1,
                width=self.price_data_list_width * 1.5,
                height=self.price_data_list_height,
                fg_color="red",
                hover_color="maroon",
                text="X",
                text_color="white",
                font=CTk.CTkFont(size=20, weight="bold"),
                command=lambda: destroy(
                    self,
                    self.products_label1,
                    self.products[0][0],
                    self.sum1,
                    self.products[0][2] * int(self.amount1.cget("text")),
                ),
            )
            self.check1.place(x=self.price_data_list_width * 13, y=0)

            # добавление продукта в список и изменение номера продукта в списке
            self.check_box_list.update({self.products[0][0]: 1})
            self.number_price_label += 1
            self.number_data_list.append(self.number1)


# удаление продукта из списка и уменьшение итоговой суммы
def destroy(self, check, name, price, weight) -> None:
    # вычет из итога цены продукта
    self.total_price.configure(
        text=str(self.total_price.cget("text").split(": ")[0])
        + ": "
        + str(
            round(
                (
                    float(self.total_price.cget("text").split(": ")[1])
                    - float(price.cget("text"))
                ),
                2,
            )
        )
    )

    # вычет из итога с процентами цену продукта
    self.total_percent_price.configure(
        text=(
            str(self.total_percent_price.cget("text").split(": ")[0])
            + ": "
            + str(
                round(
                    (
                        # float(self.total_price.cget("text").split(": ")[1])
                        # - float(
                        #     (
                        #         (float(self.total_price.cget("text").split(": ")[1]))
                        #         / 100
                        #     )
                        #     * float(
                        #         self.total_percent.cget("text")
                        #         .split(": ")[1]
                        #         .replace("%", "")
                        #     )
                        float(self.total_price.cget("text").split(": ")[1])
                        * (
                            1
                            + (
                                float(
                                    self.total_percent.cget("text")
                                    .split(": ")[1]
                                    .replace("%", "")
                                )
                                / 100
                            )
                        )
                    ),
                    2,
                )
            )
        )
    )

    # вычет из суммы вес продукта
    self.total_weight.configure(
        text=str(
            str(self.total_weight.cget("text").split(": ")[0])
            + ": "
            + str(int(float(self.total_weight.cget("text").split(": ")[1]) - weight))
        )
    )

    # удаление продукта из списка
    check.destroy()
    self.number_price_label -= 1
    self.check_box_list.pop(name)
    self.number_data_list[-1].destroy()
    self.number_data_list.pop()
