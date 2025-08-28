from argparse import ArgumentParser
from asyncio import create_subprocess_exec
from asyncio import run as aiorun
from asyncio.subprocess import PIPE
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import run as cmd
from sys import executable as python_version

import aiofiles

__all__ = ["AsyncPackageManager", "SyncPackageManager"]


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

    def run_command(self, command: list[str]) -> bool:
        """
        Запускает команду в подпроцессе.

        Args:
            command (list[str]): Команда для выполнения.

        Returns:
            bool: True, если команда выполнена успешно, иначе False.
        """
        try:
            cmd(command, check=True, capture_output=True, text=True)
            return True
        except CalledProcessError as exception:
            print(  # noqa: T201
                f"Ошибка при выполнении команды {' '.join(command)}: {exception.stderr}"  # noqa: E501
            )
            return False

    def read_requirements(self) -> list[str]:
        """
        Читает файл requirements.txt и возвращает список библиотек.

        Returns:
            list[str]: Список библиотек.
        """
        try:
            with open(self.requirements_file, encoding="utf-8") as file:
                return [
                    line.strip()
                    for line in file.readlines()
                    if line.strip() and line[0] != "#"
                ]
        except FileNotFoundError:
            print(f"Файл {self.requirements_file} не найден")  # noqa: T201
            return []

    def get_installed_packages(self) -> list[str]:
        """
        Возвращает список установленных библиотек.

        Returns:
            list[str]: Список установленных библиотек.
        """
        result = cmd(
            [python_version, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            check=False,
        )
        return [
            pkg.split("==")[0].lower() for pkg in result.stdout.splitlines()
        ]

    def get_outdated_packages(self) -> list[str]:
        """
        Возвращает список устаревших библиотек.

        Returns:
            list[str]: Список устаревших библиотек.
        """
        result = cmd(
            [
                python_version,
                "-m",
                "pip",
                "list",
                "--outdated",
                "--format=freeze",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        return [
            pkg.split("==")[0].lower() for pkg in result.stdout.splitlines()
        ]

    def install(self, packages: list[str]) -> None:
        """
        Устанавливает библиотеки, пропуская уже установленные.

        Args:
            packages (list[str]): Список библиотек для установки.
        """
        installed_packages = self.get_installed_packages()
        for package in packages:
            if package.lower() in installed_packages:
                print(  # noqa: T201
                    f"Библиотека {package} уже установлена. Пропускаем..."
                )
                continue
            print(f"Установка библиотеки {package}...", end="")  # noqa: T201
            if self.run_command(
                [python_version, "-m", "pip", "install", package]
            ):
                print(  # noqa: T201
                    f"\rБиблиотека {package} установлена"  # noqa: RUF001
                )
            else:
                print(  # noqa: T201
                    f"\rБиблиотека {package} не установлена"  # noqa: RUF001
                )

    def update(self) -> None:
        """Обновляет только устаревшие библиотеки."""
        outdated_packages = self.get_outdated_packages()
        if not outdated_packages:
            print("Все библиотеки актуальны.")  # noqa: RUF001, T201
            return

        for package in outdated_packages:
            print(f"Обновление библиотеки {package}...", end="")  # noqa: T201
            if self.run_command(
                [python_version, "-m", "pip", "install", "--upgrade", package]
            ):
                print(f"\rБиблиотека {package} обновлена")  # noqa: RUF001, T201
            else:
                print(  # noqa: T201
                    f"\rБиблиотека {package} не обновлена"  # noqa: RUF001
                )


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

    async def run_command(self, command: list[str]) -> bool:
        """
        Асинхронно запускает команду в подпроцессе.

        Args:
            command (list[str]): Команда для выполнения.

        Returns:
            bool: True, если команда выполнена успешно, иначе False.
        """
        try:
            process = await create_subprocess_exec(
                *command, stdout=PIPE, stderr=PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                print(  # noqa: T201
                    f"Ошибка при выполнении команды {' '.join(command)}: {stderr.decode()}"  # noqa: E501
                )
                return False
            return True
        except Exception as exception:
            print(  # noqa: T201
                f"Ошибка при выполнении команды {' '.join(command)}: {exception}"  # noqa: E501
            )
            return False

    async def read_requirements(self) -> list[str]:
        """
        Асинхронно читает файл requirements.txt и возвращает список библиотек.

        Returns:
            list[str]: Список библиотек.
        """
        try:
            async with aiofiles.open(
                self.requirements_file, encoding="utf-8"
            ) as file:
                lines = await file.readlines()
                return [
                    line.strip()
                    for line in lines
                    if line.strip() and line[0] != "#"
                ]
        except FileNotFoundError:
            print(f"Файл {self.requirements_file} не найден")  # noqa: T201
            return []

    async def get_installed_packages(self) -> list[str]:
        """
        Асинхронно возвращает список установленных библиотек.

        Returns:
            list[str]: Список установленных библиотек.
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
        return [
            pkg.split("==")[0].lower() for pkg in stdout.decode().splitlines()
        ]

    async def get_outdated_packages(self) -> list[str]:
        """
        Асинхронно возвращает список устаревших библиотек.

        Returns:
            list[str]: Список устаревших библиотек.
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
        return [
            pkg.split("==")[0].lower() for pkg in stdout.decode().splitlines()
        ]

    async def install(self, packages: list[str]) -> None:
        """
        Асинхронно устанавливает библиотеки, пропуская уже установленные.

        Args:
            packages (list[str]): Список библиотек для установки.
        """
        installed_packages = await self.get_installed_packages()
        for package in packages:
            if package.lower() in installed_packages:
                print(  # noqa: T201
                    f"Библиотека {package} уже установлена. Пропускаем..."
                )
                continue
            print(f"Установка библиотеки {package}...", end="")  # noqa: T201
            if await self.run_command(
                [python_version, "-m", "pip", "install", package]
            ):
                print(  # noqa: T201
                    f"\rБиблиотека {package} установлена"  # noqa: RUF001
                )
            else:
                print(  # noqa: T201
                    f"\rБиблиотека {package} не установлена"  # noqa: RUF001
                )

    async def update(self) -> None:
        """Асинхронно обновляет только устаревшие библиотеки."""
        outdated_packages = await self.get_outdated_packages()
        if not outdated_packages:
            print("Все библиотеки актуальны.")  # noqa: RUF001, T201
            return

        for package in outdated_packages:
            print(f"Обновление библиотеки {package}...", end="")  # noqa: T201
            if await self.run_command(
                [python_version, "-m", "pip", "install", "--upgrade", package]
            ):
                print(f"\rБиблиотека {package} обновлена")  # noqa: RUF001, T201
            else:
                print(  # noqa: T201
                    f"\rБиблиотека {package} не обновлена"  # noqa: RUF001
                )


async def main() -> None:
    """
    Основная функция для обработки аргументов командной строки.
    """
    arg_parse = ArgumentParser()
    arg_parse.add_argument(
        "-m",
        "--mode",
        choices=["sync", "async"],
        default="sync",
        help="Режим работы (синхронный или асинхронный)",
    )
    arg_parse.add_argument(
        "-r",
        "--requirements",
        default="./requirements.txt",
        help="Путь к файлу requirements.txt с библиотеками",  # noqa: RUF001
    )
    args = arg_parse.parse_args()
    requirements_path = Path(args.requirements or "./requirements.txt")
    manager = (
        SyncPackageManager(requirements_path)
        if args.mode == "sync"
        else AsyncPackageManager(requirements_path)
    )

    try:
        print("Начало установки библиотек...")  # noqa: T201
        if isinstance(manager, SyncPackageManager):
            manager.install(manager.read_requirements())
            print("Начало обновления библиотек...")  # noqa: T201
            manager.update()
        else:
            await manager.install(await manager.read_requirements())
            print("Начало обновления библиотек...")  # noqa: T201
            await manager.update()
        print("Процесс завершен")  # noqa: T201
    except KeyboardInterrupt:
        print("\nВыход...")  # noqa: RUF001, T201


if __name__ == "__main__":
    aiorun(main())
