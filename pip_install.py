from subprocess import run

# from tqdm import tqdm
from sys import executable as python_version

# from pypi_simple import PyPISimple


class PIP:
    def __init__(
        self, file_path: str, install_requirements: bool = True, update_all: bool = True
    ) -> None:
        self.__update("pip")
        if install_requirements:
            requirements_packages: list[str] = (
                open(file_path, "r", encoding="utf-8").read().split("\n")
            )
            print(
                f"Начало скачивания пакетов из файла {file_path.split("\\")[-1].split("/")[-1]}"
            )
            print("\n\n")
            for id_, requirements_package_name in enumerate(requirements_packages):
                print(
                    f"Скачивание {requirements_package_name}... [{id_+1}/{len(requirements_packages)}]"
                )
                self.__install_update(requirements_package_name)
                print("\n")
            print("\n")
            print(
                f"Пакеты из файла {file_path.split("\\")[-1].split("/")[-1]} успешно скачаны"
            )
        if install_requirements and update_all:
            print("\n\n\n")
        if update_all:
            print("Начало обновления установленных пакетов")
            print("\n\n")
            packages_to_update = run(
                [python_version, "-m", "pip", "list", "--outdated"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            print(packages_to_update)
            # for package_to_update in packages_to_update:
            #     print(f"Обновление {package_to_update}...")
            #     self.__update(package_to_update)
            #     print("\n")
            # print("\n")
            # print("Установленные пакеты успешно обновлены")

    def __install(self, package: str) -> bool:
        try:
            run(
                [python_version, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Пакет {package} успешно установлен")
            return True
        except Exception as e:
            print(f"Error from {package}: {e}")
            return False

    def __update(self, package: str) -> bool:
        try:
            run(
                [python_version, "-m", "pip", "install", "--upgrade", package],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Пакет {package} успешно обновлен")
            return True
        except Exception as e:
            print(f"Error from {package}: {e}")
            return False

    def __install_update(self, package: str) -> bool:
        try:
            install_out = self.__install(package)
            update_out = self.__update(package)

            if not install_out:
                print(f"Не удалось установить пакет: {package}")
            if not update_out:
                print(f"Не удалось обновить пакет: {package}")
            if install_out and update_out:
                print(f"Пакет {package} успешно установлен и обновлен")
                return True
            return False
        except Exception as e:
            print(f"Error from {package}: {e}")
            return False

    def __get_package_data(self, package: str): ...


print(
    PIP(
        file_path="D:/python/requirements.txt",
        install_requirements=False,
        update_all=False,
    ).__get_package_data("aiogram")
)
