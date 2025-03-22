from subprocess import run as cmd, CalledProcessError
from sys import executable as python_version, argv as cmd_args
from pathlib import Path
from asyncio import create_subprocess_exec, run as aiorun
from asyncio.subprocess import PIPE
from typing import List
from argparse import ArgumentParser
import aiofiles

__all__ = ["SyncPackageManager", "AsyncPackageManager"]


class SyncPackageManager:
    """
    Синхронный менеджер пакетов для установки и обновления библиотек.
    """

    def __init__(
        self, requirements_file_path: Path = Path("./requirements.txt")
    ) -> None:
        """
        Инициализация SyncPackageManager.

        Args:
            requirements_file_path (Path): Путь к файлу requirements.txt.
        """
        self.requirements_file = requirements_file_path

    def run_command(self, command: List[str]) -> bool:
        """
        Запускает команду в подпроцессе.

        Args:
            command (List[str]): Команда для выполнения.

        Returns:
            bool: True, если команда выполнена успешно, иначе False.
        """
        try:
            cmd(command, check=True, capture_output=True, text=True)
            return True
        except CalledProcessError as exception:
            print(
                f"Ошибка при выполнении команды {' '.join(command)}: {exception.stderr}"
            )
            return False

    def read_requirements(self) -> List[str]:
        """
        Читает файл requirements.txt и возвращает список библиотек.

        Returns:
            List[str]: Список библиотек.
        """
        try:
            with open(self.requirements_file, "r", encoding="utf-8") as file:
                return [
                    line.strip()
                    for line in file.readlines()
                    if line.strip() and line[0] != "#"
                ]
        except FileNotFoundError:
            print(f"Файл {self.requirements_file} не найден")
            return []

    def get_installed_packages(self) -> List[str]:
        """
        Возвращает список установленных библиотек.

        Returns:
            List[str]: Список установленных библиотек.
        """
        result = cmd(
            [python_version, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
        )
        return [pkg.split("==")[0].lower() for pkg in result.stdout.splitlines()]

    def get_outdated_packages(self) -> List[str]:
        """
        Возвращает список устаревших библиотек.

        Returns:
            List[str]: Список устаревших библиотек.
        """
        result = cmd(
            [python_version, "-m", "pip", "list", "--outdated", "--format=freeze"],
            capture_output=True,
            text=True,
        )
        return [pkg.split("==")[0].lower() for pkg in result.stdout.splitlines()]

    def install(self, packages: List[str]) -> None:
        """
        Устанавливает библиотеки, пропуская уже установленные.

        Args:
            packages (List[str]): Список библиотек для установки.
        """
        installed_packages = self.get_installed_packages()
        for package in packages:
            if package.lower() in installed_packages:
                print(f"Библиотека {package} уже установлена. Пропускаем...")
                continue
            print(f"Установка библиотеки {package}...", end="")
            if self.run_command([python_version, "-m", "pip", "install", package]):
                print(f"\rБиблиотека {package} установлена")
            else:
                print(f"\rБиблиотека {package} не установлена")

    def update(self) -> None:
        """Обновляет только устаревшие библиотеки."""
        outdated_packages = self.get_outdated_packages()
        if not outdated_packages:
            print("Все библиотеки актуальны.")
            return

        for package in outdated_packages:
            print(f"Обновление библиотеки {package}...", end="")
            if self.run_command(
                [python_version, "-m", "pip", "install", "--upgrade", package]
            ):
                print(f"\rБиблиотека {package} обновлена")
            else:
                print(f"\rБиблиотека {package} не обновлена")


class AsyncPackageManager:
    """
    Асинхронный менеджер пакетов для установки и обновления библиотек.
    """

    def __init__(
        self, requirements_file_path: Path = Path("./requirements.txt")
    ) -> None:
        """
        Инициализация AsyncPackageManager.

        Args:
            requirements_file_path (Path): Путь к файлу requirements.txt.
        """
        self.requirements_file = requirements_file_path

    async def run_command(self, command: List[str]) -> bool:
        """
        Асинхронно запускает команду в подпроцессе.

        Args:
            command (List[str]): Команда для выполнения.

        Returns:
            bool: True, если команда выполнена успешно, иначе False.
        """
        try:
            process = await create_subprocess_exec(*command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                print(
                    f"Ошибка при выполнении команды {' '.join(command)}: {stderr.decode()}"
                )
                return False
            return True
        except Exception as exception:
            print(f"Ошибка при выполнении команды {' '.join(command)}: {exception}")
            return False

    async def read_requirements(self) -> List[str]:
        """
        Асинхронно читает файл requirements.txt и возвращает список библиотек.

        Returns:
            List[str]: Список библиотек.
        """
        try:
            async with aiofiles.open(
                self.requirements_file, mode="r", encoding="utf-8"
            ) as file:
                lines = await file.readlines()
                return [
                    line.strip() for line in lines if line.strip() and line[0] != "#"
                ]
        except FileNotFoundError:
            print(f"Файл {self.requirements_file} не найден")
            return []

    async def get_installed_packages(self) -> List[str]:
        """
        Асинхронно возвращает список установленных библиотек.

        Returns:
            List[str]: Список установленных библиотек.
        """
        process = await create_subprocess_exec(
            python_version,
            "-m",
            "pip",
            "list",
            "--format=freeze",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, _ = await process.communicate()
        return [pkg.split("==")[0].lower() for pkg in stdout.decode().splitlines()]

    async def get_outdated_packages(self) -> List[str]:
        """
        Асинхронно возвращает список устаревших библиотек.

        Returns:
            List[str]: Список устаревших библиотек.
        """
        process = await create_subprocess_exec(
            python_version,
            "-m",
            "pip",
            "list",
            "--outdated",
            "--format=freeze",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, _ = await process.communicate()
        return [pkg.split("==")[0].lower() for pkg in stdout.decode().splitlines()]

    async def install(self, packages: List[str]) -> None:
        """
        Асинхронно устанавливает библиотеки, пропуская уже установленные.

        Args:
            packages (List[str]): Список библиотек для установки.
        """
        installed_packages = await self.get_installed_packages()
        for package in packages:
            if package.lower() in installed_packages:
                print(f"Библиотека {package} уже установлена. Пропускаем...")
                continue
            print(f"Установка библиотеки {package}...", end="")
            if await self.run_command(
                [python_version, "-m", "pip", "install", package]
            ):
                print(f"\rБиблиотека {package} установлена")
            else:
                print(f"\rБиблиотека {package} не установлена")

    async def update(self) -> None:
        """Асинхронно обновляет только устаревшие библиотеки."""
        outdated_packages = await self.get_outdated_packages()
        if not outdated_packages:
            print("Все библиотеки актуальны.")
            return

        for package in outdated_packages:
            print(f"Обновление библиотеки {package}...", end="")
            if await self.run_command(
                [python_version, "-m", "pip", "install", "--upgrade", package]
            ):
                print(f"\rБиблиотека {package} обновлена")
            else:
                print(f"\rБиблиотека {package} не обновлена")


async def main() -> None:
    """
    Основная функция для обработки аргументов командной строки.
    """
    args = ArgumentParser()
    args.add_argument(
        "-m",
        "--mode",
        choices=["sync", "async"],
        default="sync",
        help="Режим работы (синхронный или асинхронный)",
    )
    args.add_argument(
        "-r",
        "--requirements",
        default="./requirements.txt",
        help="Путь к файлу requirements.txt с библиотеками",
    )
    args = args.parse_args()
    requirements_path = Path(
        args.requirements if args.requirements else "./requirements.txt"
    )
    manager = (
        SyncPackageManager(requirements_path)
        if args.mode == "sync"
        else AsyncPackageManager(requirements_path)
    )

    try:
        print("Начало установки библиотек...")
        if isinstance(manager, SyncPackageManager):
            manager.install(manager.read_requirements())
            print("Начало обновления библиотек...")
            manager.update()
        else:
            await manager.install(await manager.read_requirements())
            print("Начало обновления библиотек...")
            await manager.update()
        print("Процесс завершен")
    except KeyboardInterrupt:
        print("\nВыход...")


if __name__ == "__main__":
    aiorun(main())
