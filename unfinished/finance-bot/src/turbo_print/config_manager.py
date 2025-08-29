import json
import logging
from io import StringIO
from pathlib import Path
from typing import Any

from yaml import YAMLError
from yaml import dump as yaml_dump
from yaml import safe_load as yaml_load

from .filters.composite import CompositeFilter
from .filters.regex import RegexFilter
from .formatters.simple import SimpleFormatter
from .handlers.stream import StreamHandler
from .logger import TurboLogger


class LoggerSchema:
    """Схема для работы с конфигурацией логгера TurboLogger."""

    @classmethod
    def get_handlers(cls, logger: TurboLogger) -> dict[str, Any]:
        """Получить конфигурацию всех обработчиков логгера."""
        data: dict[str, Any] = {}

        handlers = logger.get_handlers()
        if not handlers:
            return data

        for handler in handlers:
            handler_name = handler.__class__.__name__
            data[handler_name] = {}

            # Конфигурация форматтера
            if handler.formatter:
                data[handler_name]["formatter"] = cls._serialize_formatter(
                    handler.formatter
                )
            else:
                data[handler_name]["formatter"] = None

            # Уровень логирования
            data[handler_name]["level"] = handler.level.name

            # Остальные параметры обработчика
            handler_args = handler.__dict__.copy()
            handler_args.pop("formatter", None)
            handler_args.pop("level", None)

            for arg_name, arg_value in handler_args.items():
                data[handler_name][arg_name] = cls._serialize_value(arg_value)

        return dict(sorted(data.items(), key=lambda kv: kv[0]))

    @classmethod
    def get_formatter(cls, logger: TurboLogger) -> dict[str, Any]:
        """Получить конфигурацию форматтера логгера."""
        data: dict[str, Any] = {}

        formatter = logger.get_formatter()
        if not formatter:
            return data

        return cls._serialize_formatter(formatter)

    @classmethod
    def get_filters(cls, logger: TurboLogger) -> list[dict[str, Any]]:
        """Получить конфигурацию всех фильтров логгера."""
        data: list[dict[str, Any]] = []

        filters = logger.get_filters()
        if not filters:
            return data

        for filter_obj in filters:
            filter_data = {
                "name": filter_obj.__class__.__name__,
                "parameters": {},
            }

            # Сериализация параметров фильтра
            filter_args = filter_obj.__dict__.copy()
            for arg_name, arg_value in filter_args.items():
                filter_data["parameters"][arg_name] = cls._serialize_value(
                    arg_value
                )

            data.append(filter_data)

        return data

    @classmethod
    def get_middlewares(cls, logger: TurboLogger) -> list[dict[str, Any]]:
        """Получить конфигурацию всех middleware логгера."""
        data: list[dict[str, Any]] = []

        middlewares = logger.get_middlewares()
        if not middlewares:
            return data

        for middleware in middlewares:
            middleware_data = {
                "name": middleware.__class__.__name__,
                "parameters": {},
            }

            # Сериализация параметров middleware
            middleware_args = middleware.__dict__.copy()
            for arg_name, arg_value in middleware_args.items():
                middleware_data["parameters"][arg_name] = cls._serialize_value(
                    arg_value
                )

            data.append(middleware_data)

        return data

    @classmethod
    def get_context(cls, logger: TurboLogger) -> dict[str, Any]:
        """Получить контекст логгера."""
        return logger.get_context().copy()

    @classmethod
    def import_schema(cls, logger: TurboLogger) -> dict[str, Any]:
        """Импортировать полную схему логгера."""
        data: dict[str, Any] = {}

        # Основные параметры
        data["name"] = logger.get_name()
        data["level"] = logger.get_level().name
        data["propagate"] = getattr(logger, "_propagate", True)

        # Компоненты логгера
        data["handlers"] = cls.get_handlers(logger)
        data["formatter"] = cls.get_formatter(logger)
        data["filters"] = cls.get_filters(logger)
        data["middlewares"] = cls.get_middlewares(logger)
        data["context"] = cls.get_context(logger)

        # Информация о родительском логгере
        if hasattr(logger, "parent") and logger.parent:
            data["parent"] = logger.parent.get_name()
        else:
            data["parent"] = None

        return dict(sorted(data.items(), key=lambda kv: kv[0]))

    @classmethod
    def _serialize_formatter(cls, formatter: Any) -> dict[str, Any]:
        """Сериализовать форматтер в словарь."""
        data: dict[str, Any] = {}

        if not formatter:
            return data

        data["name"] = formatter.__class__.__name__

        # Сериализация параметров форматтера
        formatter_args = formatter.__dict__.copy()
        for arg_name, arg_value in formatter_args.items():
            data[arg_name] = cls._serialize_value(arg_value)

        return dict(sorted(data.items(), key=lambda kv: kv[0]))

    @classmethod
    def _serialize_value(cls, value: Any) -> Any:
        """Безопасно сериализовать значение для YAML/JSON."""
        if value is None:
            return None

        try:
            # Проверяем, можно ли сериализовать в YAML
            yaml_dump(value, StringIO())
            return value
        except (TypeError, YAMLError):
            # Если не удается сериализовать, возвращаем строковое представление
            return repr(value)


class ConfigManager:
    """Менеджер конфигурации для работы с файлами различных форматов."""

    SUPPORTED_FORMATS = {
        "yaml": [".yaml", ".yml"],
        "json": [".json"],
        "config": [".config", ".cfg"],
        "settings": [".settings", ".ini"],
        "env": [".env"],
        "database": [".db", ".sqlite", ".sqlite3"],
    }

    def __init__(self, file_path: str | Path) -> None:
        """
        Инициализация менеджера конфигурации.

        Args:
            file_path: Путь к файлу конфигурации
        """
        self.file_path = Path(file_path)
        self._validate_file_format()
        self._ensure_file_exists()

    def _validate_file_format(self) -> None:
        """Проверить поддерживаемый формат файла."""
        file_extension = self.file_path.suffix.lower()
        supported_extensions = [
            ext
            for extensions in self.SUPPORTED_FORMATS.values()
            for ext in extensions
        ]

        if file_extension not in supported_extensions:
            raise ValueError(
                f"Неподдерживаемый формат файла: {file_extension}. "
                f"Поддерживаемые форматы: {', '.join(supported_extensions)}"
            )

    def _ensure_file_exists(self) -> None:
        """Создать файл и директории, если они не существуют."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch(exist_ok=True)

    def _get_file_format(self) -> str:
        """Определить формат файла."""
        file_extension = self.file_path.suffix.lower()

        for format_name, extensions in self.SUPPORTED_FORMATS.items():
            if file_extension in extensions:
                return format_name

        return "unknown"

    def import_config(self) -> dict[str, Any]:
        """
        Импортировать конфигурацию из файла.

        Returns:
            Словарь с конфигурацией или пустой словарь при ошибке
        """
        file_format = self._get_file_format()

        try:
            if file_format == "yaml":
                return self._import_yaml()
            elif file_format == "json":
                return self._import_json()
            elif file_format == "env":
                return self._import_env()
            else:
                logging.warning(
                    f"Формат {file_format} не поддерживается для импорта"
                )
                return {}

        except Exception as e:
            logging.error(f"Ошибка импорта конфигурации: {e}")
            return {}

    def export_config(self, data: dict[str, Any]) -> bool:
        """
        Экспортировать конфигурацию в файл.

        Args:
            data: Данные для экспорта

        Returns:
            True если экспорт успешен, False в противном случае
        """
        file_format = self._get_file_format()

        try:
            if file_format == "yaml":
                return self._export_yaml(data)
            elif file_format == "json":
                return self._export_json(data)
            elif file_format == "env":
                return self._export_env(data)
            else:
                logging.warning(
                    f"Формат {file_format} не поддерживается для экспорта"
                )
                return False

        except Exception as e:
            logging.error(f"Ошибка экспорта конфигурации: {e}")
            return False

    def _import_yaml(self) -> dict[str, Any]:
        """Импортировать конфигурацию из YAML файла."""
        try:
            with open(self.file_path, encoding="utf-8") as file:
                config = yaml_load(file)
                return config if config else {}
        except YAMLError as e:
            logging.error(f"Ошибка парсинга YAML: {e}")
            return {}
        except Exception as e:
            logging.error(f"Ошибка чтения YAML файла: {e}")
            return {}

    def _export_yaml(self, data: dict[str, Any]) -> bool:
        """Экспортировать конфигурацию в YAML файл."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml_dump(
                    data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2,
                    width=120,
                )
            return True
        except Exception as e:
            logging.error(f"Ошибка записи YAML файла: {e}")
            return False

    def _import_json(self) -> dict[str, Any]:
        """Импортировать конфигурацию из JSON файла."""
        try:
            with open(self.file_path, encoding="utf-8") as file:
                config = json.load(file)
                return config if config else {}
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка парсинга JSON: {e}")
            return {}
        except Exception as e:
            logging.error(f"Ошибка чтения JSON файла: {e}")
            return {}

    def _export_json(self, data: dict[str, Any]) -> bool:
        """Экспортировать конфигурацию в JSON файл."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(
                    data, file, ensure_ascii=False, indent=2, sort_keys=False
                )
            return True
        except Exception as e:
            logging.error(f"Ошибка записи JSON файла: {e}")
            return False

    def _import_env(self) -> dict[str, Any]:
        """Импортировать конфигурацию из .env файла."""
        config = {}
        try:
            with open(self.file_path, encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip().strip("\"'")
            return config
        except Exception as e:
            logging.error(f"Ошибка чтения .env файла: {e}")
            return {}

    def _export_env(self, data: dict[str, Any]) -> bool:
        """Экспортировать конфигурацию в .env файл."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                for key, value in data.items():
                    if isinstance(value, str):
                        file.write(f'{key}="{value}"\n')
                    else:
                        file.write(f"{key}={value}\n")
            return True
        except Exception as e:
            logging.error(f"Ошибка записи .env файла: {e}")
            return False

    def validate_config(self, config: dict[str, Any]) -> list[str]:
        """
        Валидировать конфигурацию.

        Args:
            config: Конфигурация для валидации

        Returns:
            Список ошибок валидации (пустой если валидация прошла успешно)
        """
        errors = []

        # Проверка обязательных полей
        required_fields = ["level"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Отсутствует обязательное поле: {field}")

        # Проверка уровня логирования
        if "level" in config:
            level = config["level"]
            valid_levels = [
                "NOTSET",
                "DEBUG",
                "LOG",
                "SUCCESS",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
                "FATAL",
            ]
            if level not in valid_levels:
                errors.append(f"Недопустимый уровень логирования: {level}")

        # Проверка handlers
        if "handlers" in config and not isinstance(config["handlers"], dict):
            errors.append("Поле 'handlers' должно быть словарем")

        # Проверка formatter
        if "formatter" in config and not isinstance(
            config["formatter"], dict | type(None)
        ):
            errors.append("Поле 'formatter' должно быть словарем или None")

        return errors

    def get_config_info(self) -> dict[str, Any]:
        """
        Получить информацию о файле конфигурации.

        Returns:
            Словарь с информацией о файле
        """
        return {
            "file_path": str(self.file_path),
            "file_format": self._get_file_format(),
            "file_size": (
                self.file_path.stat().st_size if self.file_path.exists() else 0
            ),
            "exists": self.file_path.exists(),
            "supported_formats": self.SUPPORTED_FORMATS,
        }

    @classmethod
    def import_schema(cls, logger: TurboLogger) -> dict[str, Any]:
        """
        Импортировать схему логгера.

        Args:
            logger: Экземпляр TurboLogger

        Returns:
            Схема логгера
        """
        return LoggerSchema.import_schema(logger)

    @classmethod
    def create_from_schema(
        cls, schema: dict[str, Any], file_path: str | Path
    ) -> "ConfigManager":
        """
        Создать ConfigManager из схемы и экспортировать в файл.

        Args:
            schema: Схема логгера
            file_path: Путь к файлу конфигурации

        Returns:
            Экземпляр ConfigManager
        """
        config_manager = cls(file_path)
        config_manager.export_config(schema)
        return config_manager
