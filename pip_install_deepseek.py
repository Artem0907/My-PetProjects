import asyncio
import logging
import subprocess
import argparse
from typing import List, Optional, Set


class SyncPackageManager:
    """Синхронный менеджер пакетов для установки и обновления."""

    def __init__(self, requirements_file: str, log_level: int = logging.INFO):
        """
        Инициализация синхронного менеджера пакетов.

        Args:
            requirements_file (str): Путь к файлу requirements.txt.
            log_level (int): Уровень логирования. По умолчанию INFO.
        """
        self.requirements_file = requirements_file
        self.logger = self._setup_logger(log_level)
        self._outdated_packages: Optional[Set[str]] = None  # Кеш для устаревших пакетов

    def _setup_logger(self, log_level: int) -> logging.Logger:
        """Настройка логгера для вывода в консоль."""
        logger = logging.getLogger("SyncPackageManager")
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _run_command(self, command: List[str]) -> Optional[str]:
        """Запуск команды в синхронном режиме."""
        self.logger.debug(f"Запуск команды: {command}")
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            self.logger.debug(f"Команда выполнена успешно: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Ошибка при выполнении команды {command}: {e.stderr}")
            return None

    def _get_outdated_packages(self) -> Optional[Set[str]]:
        """Получение списка устаревших пакетов."""
        self.logger.debug("Получение списка устаревших пакетов...")
        if self._outdated_packages is not None:
            self.logger.debug("Использование кешированного списка устаревших пакетов.")
            return self._outdated_packages

        result = self._run_command(["pip", "list", "--outdated"])
        if result:
            outdated_packages = {line.split()[0] for line in result.splitlines()[2:]}
            self._outdated_packages = outdated_packages
            self.logger.debug(f"Найдены устаревшие пакеты: {outdated_packages}")
            return outdated_packages
        self.logger.debug("Устаревшие пакеты не найдены.")
        return None

    def install_packages(self) -> None:
        """Установка пакетов из requirements.txt."""
        self.logger.info("Начало установки пакетов...")
        result = self._run_command(["pip", "install", "-r", self.requirements_file])
        if result:
            self.logger.info("Пакеты успешно установлены.")
        else:
            self.logger.error("Ошибка при установке пакетов.")

    def update_packages(self) -> None:
        """Обновление устаревших пакетов."""
        self.logger.info("Начало обновления пакетов...")
        outdated_packages = self._get_outdated_packages()
        if outdated_packages:
            self.logger.info(
                f"Найдены устаревшие пакеты: {', '.join(outdated_packages)}"
            )
            for package in outdated_packages:
                self.logger.debug(f"Обновление пакета: {package}")
                self._run_command(["pip", "install", "--upgrade", package])
        else:
            self.logger.info("Нет устаревших пакетов.")


class AsyncPackageManager:
    """Асинхронный менеджер пакетов для установки и обновления."""

    def __init__(self, requirements_file: str, log_level: int = logging.INFO):
        """
        Инициализация асинхронного менеджера пакетов.

        Args:
            requirements_file (str): Путь к файлу requirements.txt.
            log_level (int): Уровень логирования. По умолчанию INFO.
        """
        self.requirements_file = requirements_file
        self.logger = self._setup_logger(log_level)
        self._outdated_packages: Optional[Set[str]] = None  # Кеш для устаревших пакетов

    def _setup_logger(self, log_level: int) -> logging.Logger:
        """Настройка логгера для вывода в консоль."""
        logger = logging.getLogger("AsyncPackageManager")
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def _run_command_async(self, command: List[str]) -> Optional[str]:
        """Запуск команды в асинхронном режиме."""
        self.logger.debug(f"Запуск команды: {command}")
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                self.logger.error(
                    f"Ошибка при выполнении команды {command}: {stderr.decode()}"
                )
                return None
            self.logger.debug(f"Команда выполнена успешно: {stdout.decode()}")
            return stdout.decode()
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении команды {command}: {str(e)}")
            return None

    async def _get_outdated_packages_async(self) -> Optional[Set[str]]:
        """Получение списка устаревших пакетов."""
        self.logger.debug("Получение списка устаревших пакетов...")
        if self._outdated_packages is not None:
            self.logger.debug("Использование кешированного списка устаревших пакетов.")
            return self._outdated_packages

        result = await self._run_command_async(["pip", "list", "--outdated"])
        if result:
            outdated_packages = {line.split()[0] for line in result.splitlines()[2:]}
            self._outdated_packages = outdated_packages
            self.logger.debug(f"Найдены устаревшие пакеты: {outdated_packages}")
            return outdated_packages
        self.logger.debug("Устаревшие пакеты не найдены.")
        return None

    async def install_packages_async(self) -> None:
        """Асинхронная установка пакетов из requirements.txt."""
        self.logger.info("Начало асинхронной установки пакетов...")
        result = await self._run_command_async(
            ["pip", "install", "-r", self.requirements_file]
        )
        if result:
            self.logger.info("Пакеты успешно установлены.")
        else:
            self.logger.error("Ошибка при установке пакетов.")

    async def update_packages_async(self) -> None:
        """Асинхронное обновление устаревших пакетов."""
        self.logger.info("Начало асинхронного обновления пакетов...")
        outdated_packages = await self._get_outdated_packages_async()
        if outdated_packages:
            self.logger.info(
                f"Найдены устаревшие пакеты: {', '.join(outdated_packages)}"
            )
            for package in outdated_packages:
                self.logger.debug(f"Обновление пакета: {package}")
                await self._run_command_async(["pip", "install", "--upgrade", package])
        else:
            self.logger.info("Нет устаревших пакетов.")


def main():
    """Основная функция для обработки аргументов командной строки и запуска менеджера."""
    parser = argparse.ArgumentParser(
        description="Установка и обновление пакетов из requirements.txt."
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["sync", "async"],
        default="sync",
        help="Режим работы: синхронный (sync) или асинхронный (async). По умолчанию: sync.",
    )
    parser.add_argument(
        "-r",
        "--requirements",
        type=str,
        default="./requirements.txt",
        help="Путь к файлу requirements.txt. По умолчанию: ./requirements.txt.",
    )
    parser.add_argument(
        "-ll",
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Уровень логирования. По умолчанию: INFO.",
    )
    args = parser.parse_args()

    log_level = getattr(logging, args.log_level)

    if args.mode == "sync":
        manager = SyncPackageManager(args.requirements, log_level)
        manager.install_packages()
        manager.update_packages()
    else:
        manager = AsyncPackageManager(args.requirements, log_level)
        asyncio.run(manager.install_packages_async())
        asyncio.run(manager.update_packages_async())


if __name__ == "__main__":
    main()
