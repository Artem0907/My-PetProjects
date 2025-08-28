from dataclasses import dataclass
from os import getenv as get_env
from os.path import exists
from pathlib import Path
from pprint import pprint
from typing import Literal

from aiogram.utils.token import validate_token
from dotenv import load_dotenv

base_env_dir = Path(__file__).parent.parent / ".env"


@dataclass
class Database:
    url: str


@dataclass
class Logs:
    dir: Path
    level: Literal[
        "NOTSET", "DEBUG", "LOG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ]
    language: Literal["ru", "en"]
    format: str
    file_max_size: int
    backup_count: int
    daily_rotation: bool
    enable_aiogram_logs: bool


@dataclass
class Bot:
    token: str
    admins: list[int]
    creator: int
    command_prefix: Literal["/", "!", "."]
    parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] | None


@dataclass
class Settings:
    language: Literal["ru", "en"]
    timezone: str
    bot: Bot
    logs: Logs
    database: Database


def get_database_settings(env_file: Path | str = base_env_dir) -> Database:
    if exists(env_file):
        load_dotenv(env_file)

    database_url = get_env("DATABASE_URL", "sqlite://db.sql").strip()

    return Database(url=database_url)


def get_logs_settings(env_file: Path | str = base_env_dir) -> Logs:
    if exists(env_file):
        load_dotenv(env_file)

    logs_dir: Path = get_env(
        "LOG_DIR", "logs"
    ).strip()  # type: ignore[assignment] # pyright: ignore[reportAssignmentType]
    if not logs_dir or not Path(logs_dir).is_dir():
        logs_dir = "logs"  # type: ignore[assignment] # pyright: ignore[reportAssignmentType]
    logs_dir = Path(logs_dir)

    logs_level: Literal[
        "NOTSET", "DEBUG", "LOG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = (
        get_env("LOG_LEVEL", "INFO").strip().upper()  # type: ignore[assignment]
    )  # pyright: ignore[reportAssignmentType]
    if logs_level not in [
        "NOTSET",
        "DEBUG",
        "LOG",
        "INFO",
        "WARN",
        "WARNING",
        "ERROR",
        "CRITICAL",
        "FATAL",
    ]:
        logs_level = "INFO"
    if logs_level == "WARN":  # type: ignore[comparison-overlap]
        logs_level = "WARNING"  # type: ignore[unreachable]
    elif logs_level == "FATAL":  # type: ignore[comparison-overlap]
        logs_level = "CRITICAL"  # type: ignore[unreachable]

    logs_language: Literal["ru", "en"] = (
        get_env("LOG_LANG", "ru").strip().lower()  # type: ignore[assignment]
    )  # pyright: ignore[reportAssignmentType]
    if logs_language not in ["ru", "en"]:
        logs_language = "ru"

    logs_format = get_env(
        "LOG_FORMAT",
        "[{time}] {level_name}: {message}",
    ).strip()

    logs_file_max_size = int(get_env("LOG_FILE_MAX_SIZE", "10485760").strip())

    logs_backup_count = get_env("LOG_BACKUP_COUNT", "3").strip()
    if (
        logs_backup_count.isnumeric()
        or logs_backup_count.isdigit()
        or logs_backup_count.isdecimal()
    ):
        logs_backup_count = int(logs_backup_count)  # type: ignore[assignment]
    else:
        logs_backup_count = 0  # type: ignore[assignment]

    logs_daily_rotation = (
        get_env("LOG_DAILY_ROTATION", "false").strip().lower() == "true"
    )

    logs_enable_aiogram_logs = (
        get_env("ENABLE_AIOGRAM_LOGS", "true").strip().lower() == "true"
    )

    return Logs(
        dir=logs_dir,
        level=logs_level,
        language=logs_language,
        format=logs_format,
        file_max_size=logs_file_max_size,
        backup_count=logs_backup_count,  # type: ignore[arg-type]
        daily_rotation=logs_daily_rotation,
        enable_aiogram_logs=logs_enable_aiogram_logs,
    )


def get_bot_settings(env_file: Path | str = base_env_dir) -> Bot:
    if exists(env_file):
        load_dotenv(env_file)

    bot_token = get_env("BOT_TOKEN")
    if not bot_token or not validate_token(bot_token.strip()):
        raise ValueError("Bot token is incorrect")

    creator_id = get_env("CREATOR_ID")
    if creator_id and (
        creator_id.strip().isnumeric()
        or creator_id.strip().isdecimal()
        or creator_id.strip().isdigit()
    ):
        bot_creator_id = int(creator_id.strip())
    else:
        bot_creator_id = 0

    bot_parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] | None = (
        get_env("BOT_PARSE_MODE", "null").strip().lower()  # type: ignore[assignment]
    )
    if bot_parse_mode not in ["html", "markdown", "markdownv2"]:
        bot_parse_mode = None

    bot_admins = get_env("ADMINS_ID", "").strip().split(",")
    bot_admins_id: list[int] = []
    for admin in bot_admins:
        if len(admin.strip()) > 0 and (
            admin.strip().isnumeric()
            or admin.strip().isdecimal()
            or admin.strip().isdigit()
        ):
            bot_admins_id.append(int(admin.strip()))

    bot_command_prefix: Literal["/", "!", "."] = (
        get_env("COMMAND_PREFIX", "/").strip().lower()  # type: ignore[assignment]
    )
    if bot_command_prefix not in ["/", "!", "."]:
        bot_command_prefix = "/"

    return Bot(
        token=bot_token.strip(),
        admins=bot_admins_id,
        creator=bot_creator_id,
        command_prefix=bot_command_prefix,
        parse_mode=bot_parse_mode,
    )


def get_settings(env_file: Path | str = base_env_dir) -> Settings:
    if exists(env_file):
        load_dotenv(env_file)

    language: Literal["ru", "en"] = (
        get_env("LANGUAGE", "ru").strip().lower()  # type: ignore[assignment]
    )
    if language not in ["ru", "en"]:
        language = "ru"

    timezone = get_env("TIMEZONE", "UTC").strip()
    bot = get_bot_settings(env_file)
    logs = get_logs_settings(env_file)
    database = get_database_settings(env_file)

    return Settings(
        language=language,
        timezone=timezone,
        bot=bot,
        logs=logs,
        database=database,
    )


if __name__ == "__main__":
    pprint(get_settings())
