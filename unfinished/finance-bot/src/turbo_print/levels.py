from dataclasses import dataclass

from colorama import Fore, Style


@dataclass(frozen=True)
class LogLevelStructure:
    name: str
    level: int
    color: str | None = None


class LogLevels:
    NOTSET = LogLevelStructure("NOTSET", 0, Fore.RESET)
    DEBUG = LogLevelStructure("DEBUG", 10, Fore.MAGENTA)
    LOG = LogLevelStructure("LOG", 20, Fore.CYAN)
    SUCCESS = LogLevelStructure("SUCCESS", 30, Fore.GREEN)
    INFO = LogLevelStructure("INFO", 40, Fore.LIGHTBLUE_EX)
    WARNING = LogLevelStructure("WARNING", 50, Fore.RED)
    ERROR = LogLevelStructure("ERROR", 60, Fore.LIGHTRED_EX)
    CRITICAL = LogLevelStructure(
        "CRITICAL", 70, Style.BRIGHT + Fore.LIGHTRED_EX
    )
    FATAL = LogLevelStructure("FATAL", 80, Style.BRIGHT + Fore.MAGENTA)


def register_level(name: str, level: int, color: str | None = None) -> None:
    clean_name = name.strip().upper()
    setattr(LogLevels, clean_name, LogLevelStructure(clean_name, level, color))


def get_all_levels() -> dict[str, LogLevelStructure]:
    levels = {
        k: v
        for k, v in LogLevels.__dict__.items()
        if not k.startswith(("_", "__"))
        and not k.endswith(("_", "__"))
        and isinstance(v, LogLevelStructure)
    }

    seen_values = set()
    unique_levels = {}
    for key, value in levels.items():
        if value not in seen_values:
            seen_values.add(value)
            unique_levels[key] = value
    return unique_levels
