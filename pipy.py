import subprocess
import sys
from typing import List, Optional
from pathlib import Path


class PackageManager:
    """
    Класс для управления установкой и обновлением Python-библиотек.
    """

    def __init__(self, requirements_file_path: Path = Path("./requirements.txt")):
        """
        Инициализация PackageManager.

        Args:
            requirements_file (str): Путь к файлу requirements.txt. По умолчанию "requirements.txt".
        """
        self.requirements_file = requirements_file_path

    def run_command(self, command: List[str]) -> bool:
        """
        Запускает команду в подпроцессе и возвращает True, если она выполнена успешно.

        Args:
            command (List[str]): Команда для выполнения.

        Returns:
            bool: True, если команда выполнена успешно, иначе False.
        """
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды {' '.join(command)}: {e.stderr}")
            return False

    def read_requirements(self) -> Optional[List[str]]:
        """
        Читает файл requirements.txt и возвращает список библиотек.

        Returns:
            Optional[List[str]]: Список библиотек или None, если файл не найден.
        """
        try:
            with open(self.requirements_file, "r", encoding="utf-8") as file:
                return [
                    line.strip() for line in file if line.strip() and line[0] != "#"
                ]
        except FileNotFoundError:
            print(f"Файл {self.requirements_file} не найден.")
            return None

    def install_packages(self) -> None:
        """
        Устанавливает библиотеки из файла requirements.txt.
        """
        packages = self.read_requirements()
        if not packages:
            return

        for package in packages:
            print(f"Установка библиотеки {package}...")
            if not self.run_command([sys.executable, "-m", "pip", "install", package]):
                print(f"Библиотека {package} не установлена. Пропускаем...")

    def get_installed_packages(self) -> List[str]:
        """
        Возвращает список установленных библиотек.

        Returns:
            List[str]: Список установленных библиотек.
        """
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
        )
        return result.stdout.splitlines()

    def update_packages(self) -> None:
        """
        Обновляет все установленные библиотеки до последних версий.
        """
        installed_packages = self.get_installed_packages()
        for package in installed_packages:
            package_name = package.split("==")[0]
            print(f"Обновление библиотеки {package_name}...")
            if not self.run_command(
                [sys.executable, "-m", "pip", "install", "--upgrade", package_name]
            ):
                print(f"Библиотека {package_name} не обновлена. Пропускаем...")

    def run(self) -> None:
        """
        Запускает процесс установки и обновления библиотек.
        """
        print("Начало установки библиотек...")
        self.install_packages()
        print("Начало обновления библиотек...")
        self.update_packages()
        print("Процесс завершен.")


if __name__ == "__main__":
    try:
        manager = PackageManager()
        manager.run()
    except KeyboardInterrupt:
        print("Выход...")
