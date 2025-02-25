from os import listdir
from ujson import dump


def write_data(directory: str, data: tuple) -> None:
    with open(f"{directory}/json/data.json", "w") as file:
        dump(
            {
                "income": data[0],
                "expenditure": data[1],
                "shift number": data[2],
                "employs names list": data[3],
                "employs name": data[4],
            },
            file,
            ensure_ascii=False,
        )


def write_favorites(directory: str) -> None:
    return


def write_product_list(directory: str) -> None:
    return
