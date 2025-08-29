from os import getenv as get_env
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from yaml import dump as yaml_dump
from yaml import full_load as yaml_load

from ..settings import base_env_dir, get_settings
from .levels import LogLevelStructure, get_all_levels
from .logger import TurboLogger


class LoggerSchema:
    @classmethod
    def _get_format(cls, data: Any) -> Any:
        if isinstance(data, list | set | tuple):
            result = []
            for element in data:
                result.append(cls._get_format(element))
        elif isinstance(data, dict):
            result = {}  # type: ignore[assignment]
            for key, value in data.items():
                result[key] = cls._get_format(value)
        elif isinstance(data, LogLevelStructure):
            result = cls.get_level_format(data)  # type: ignore[assignment]
        else:
            try:
                yaml_dump(data)
                result = data
            except Exception:
                if hasattr(data, "__repr__"):
                    result = repr(data)  # type: ignore[assignment]
                elif hasattr(data, "__str__"):
                    result = data.__class__
                else:
                    result = "unknown"  # type: ignore[assignment]

        return result

    @classmethod
    def get_handlers(cls, logger: TurboLogger) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []
        handlers = logger.get_handlers()
        if not handlers:
            return data

        for handler in handlers:
            handler_data: dict[str, Any] = {}
            handler_data["class"] = handler.__class__
            handler_data["name"] = handler.__class__.__name__
            handler_data["level"] = handler.level.name

            if handler.formatter:
                formatter_data: dict[str, Any] = {}
                formatter_data["class"] = handler.formatter.__class__
                formatter_data["name"] = handler.formatter.__class__.__name__

                formatter_data = {
                    **formatter_data,
                    **cls._get_format(handler.__dict__),
                }

                handler_data["formatter"] = formatter_data

            handler_dict = handler.__dict__
            handler_dict.pop("level")
            handler_dict.pop("formatter")
            handler_data = {**handler_data, **cls._get_format(handler_dict)}

            data.append(handler_data)

        return data

    @classmethod
    def get_filters(cls, logger: TurboLogger) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []
        filters = logger.get_filters()
        if not filters:
            return data

        for filter in filters:
            filter_data: dict[str, Any] = {}
            filter_data["class"] = filter.__class__
            filter_data["name"] = filter.__class__.__name__

            filter_data = {**filter_data, **cls._get_format(filter.__dict__)}

            data.append(filter_data)

        return data

    @classmethod
    def get_middlewares(cls, logger: TurboLogger) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []
        middlewares = logger.get_middlewares()
        if not middlewares:
            return data

        for middleware in middlewares:
            middleware_data: dict[str, Any] = {}
            middleware_data["class"] = middleware.__class__
            middleware_data["name"] = middleware.__class__.__name__

            middleware_data = {
                **middleware_data,
                **cls._get_format(middleware.__dict__),
            }

            data.append(middleware_data)

        return data

    @classmethod
    def get_formatter(cls, logger: TurboLogger) -> dict[str, Any]:
        data: dict[str, Any] = {}
        formatter = logger.get_formatter()

        data["class"] = formatter.__class__
        data["name"] = formatter.__class__.__name__

        data = {**data, **cls._get_format(formatter.__dict__)}

        return data

    @classmethod
    def get_level_format(cls, level: LogLevelStructure) -> dict[str, Any]:
        data: dict[str, Any] = {}
        data["class"] = level.__class__
        data["name"] = level.name
        data["level"] = level.level
        data["color"] = level.color
        return data

    @classmethod
    def import_schema(cls, logger: TurboLogger) -> dict[str, Any]:
        data: dict[str, Any] = {
            "name": logger.get_name(),
            "level": cls.get_level_format(logger.get_level()),
            "propagate": logger._propagate,
            "parent": None,
            "handlers": cls.get_handlers(logger),
            "formatter": cls.get_formatter(logger),
            "filters": cls.get_filters(logger),
            "middlewares": cls.get_middlewares(logger),
            "context": {},
            "global_context": {},
        }

        if hasattr(logger, "parent") and logger.parent:
            data["parent"] = logger.parent.get_name()

        for context_name, context_value in logger.get_context().items():
            try:
                yaml_dump(context_value)
                data["context"][context_name] = context_value
            except Exception:
                if hasattr(context_value, "__repr__"):
                    data["context"][context_name] = repr(context_value)
                elif hasattr(context_value, "__str__"):
                    data["context"][context_name] = context_value.__class__

        for glc_name, glc_value in logger.get_global_context().items():
            try:
                yaml_dump(glc_value)
                data["global_context"][glc_name] = glc_value
            except Exception:
                if hasattr(glc_value, "__repr__"):
                    data["global_context"][glc_name] = repr(glc_value)
                elif hasattr(glc_value, "__str__"):
                    data["global_context"][glc_name] = str(glc_value)

        return dict(sorted(data.items(), key=lambda kv: kv[0]))


class ConfigManager:
    SUPPORTED_FORMATS = {
        "yaml": [".yaml", ".yml"],
    }

    def __init__(
        self, file_path: str | Path, env_path: str | Path = base_env_dir
    ) -> None:
        self.file_path = Path(file_path)
        self.env_path = Path(env_path)
        self._validate_file_format()

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch(exist_ok=True)

    def _set_env_var(self, data: Any) -> Any:
        if isinstance(data, list | tuple | set):
            updated_data = []
            for value in data:
                updated_data.append(self._set_env_var(value))
        elif isinstance(data, dict):
            updated_data = {}  # type: ignore[assignment]
            for key, value in data.items():
                updated_data[key] = self._set_env_var(value)
        elif isinstance(data, str):
            if data[:2] + data[-1] == "${}":
                env_var_name = data[2:-1]

                load_dotenv(self.env_path)
                env_var_value = get_env(env_var_name)
                if env_var_value:
                    updated_data = env_var_value  # type: ignore[assignment]
                else:
                    settings = get_settings(self.env_path)
                    if len(env_var_name.split(".")) > 1:
                        for var_name in env_var_name.split("."):
                            if hasattr(settings, "__dict__"):
                                settings = settings.__dict__.get(var_name)  # type: ignore[assignment]
                            else:
                                updated_data = settings  # type: ignore[assignment]
                                continue
                        updated_data = settings  # type: ignore[assignment]
                    else:
                        updated_data = settings.__dict__.get(env_var_name)  # type: ignore[assignment]
            else:
                updated_data = data  # type: ignore[assignment]
        else:
            return data
        return updated_data

    def _validate_file_format(self) -> None:
        file_extension = self.file_path.suffix.lower()
        supported_extensions = [
            ext
            for extensions in self.SUPPORTED_FORMATS.values()
            for ext in extensions
        ]

        supported_formats = "\n".join(
            f"{key}: {", ".join(value)}"
            for key, value in self.SUPPORTED_FORMATS.items()
        )

        if file_extension not in supported_extensions:
            raise ValueError(
                f"Неподдерживаемый формат файла: `{file_extension}`. "
                f"Поддерживаемые форматы:\n{supported_formats}"
            )

    def _get_file_format(self) -> str:
        """Определить формат файла."""
        file_extension = self.file_path.suffix.lower()

        for format_name, extensions in self.SUPPORTED_FORMATS.items():
            if file_extension in extensions:
                return format_name

        return "unknown"

    def import_config(self) -> dict[str, Any]:
        file_format = self._get_file_format()

        with open(self.file_path, encoding="utf-8") as file:
            if file_format == "yaml":
                file_read = yaml_load(file.read())
            else:
                raise TypeError(
                    f"Формат {file_format} не поддерживается для импорта"
                )

        return self._set_env_var(file_read) or {}

    def export_config(self, config: dict[str, Any]) -> None:
        config_errors = self.validate_config(config)
        if config_errors:
            raise ValueError(f"Некорректная конфигурация: {config_errors}")
        file_format = self._get_file_format()

        with open(self.file_path, "w", encoding="utf-8") as file:
            if file_format == "yaml":
                yaml_dump(
                    config,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=4,
                    width=120,
                )
            else:
                raise TypeError(
                    f"Формат {file_format} не поддерживается для экспорта"
                )

    @classmethod
    def validate_config(cls, config: dict[str, Any]) -> list[str] | None:
        errors = []

        required_fields = {"level": dict}
        for field_name, field_type in required_fields.items():
            if field_name not in config:
                errors.append(f"Отсутствует обязательное поле: {field_name}")
            else:
                if not isinstance(config[field_name], field_type):
                    errors.append(f"Неверный тип поля: {field_name}")

        if "level" in config:
            if config["level"]["name"].upper() not in get_all_levels().keys():
                errors.append(
                    f"Недопустимый уровень логирования: {config["level"]["name"].upper()}"
                )

        if "handlers" in config and isinstance(config["handlers"], list):
            for handler in config["handlers"]:
                if not isinstance(handler, dict):
                    errors.append(
                        f"Элемент '{handler.__class__}' в поле 'handlers' должно быть словарём"
                    )
        elif "handlers" in config:
            errors.append("Поле 'handlers' должно быть словарем")

        if "filters" in config and isinstance(config["filters"], list):
            for filter in config["filters"]:
                if not isinstance(filter, dict):
                    errors.append(
                        f"Элемент '{filter.__class__}' в поле 'filters' должно быть словарём"
                    )
        elif "filters" in config:
            errors.append("Поле 'filters' должно быть словарем")

        if "middlewares" in config and isinstance(config["middlewares"], list):
            for middleware in config["middlewares"]:
                if not isinstance(middleware, dict):
                    errors.append(
                        f"Элемент '{middleware.__class__}' в поле 'middlewares' должно быть словарём"
                    )
        elif "middlewares" in config:
            errors.append("Поле 'middlewares' должно быть словарем")

        if "formatter" in config and not isinstance(
            config["formatter"], dict | type(None)
        ):
            errors.append("Поле 'formatter' должно быть словарем или None")

        return errors or None

    @staticmethod
    def import_schema(logger: TurboLogger) -> dict[str, Any]:
        return LoggerSchema.import_schema(logger)

    def export_from_logger(self, logger: TurboLogger) -> None:
        self.export_config(LoggerSchema.import_schema(logger))
