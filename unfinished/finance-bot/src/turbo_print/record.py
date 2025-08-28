from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

from .levels import LogLevelStructure

if TYPE_CHECKING:
    from .logger import TurboLogger


@dataclass
class LogRecord:
    message: str
    level: LogLevelStructure
    logger: "TurboLogger"
    date_time: datetime = field(default_factory=datetime.now)
    extra: dict[str, Any] = field(default_factory=dict)
    module: str | None = None
    function: str | None = None
    line_no: int | None = None
