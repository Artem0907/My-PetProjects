from xmltodict import parse
from requests import get as reget


def read_currency_courses() -> dict[str, dict[str, str | float]]:
    courses = parse(reget("https://www.cbr.ru/scripts/XML_daily.asp").text)
    courses_dict = {"date": courses["ValCurs"]["@Date"]}
    for course in courses["ValCurs"]["Valute"]:
        courses_dict[course["CharCode"]] = {
            "name": course["Name"],
            "value": float(
                float(course["Value"].replace(",", ".")) / int(course["Nominal"])
            ),
        }
    return courses_dict


courses = read_currency_courses()
print(courses["USD"], courses["EUR"])
