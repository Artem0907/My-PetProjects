from ..levels import LogLevelStructure, get_all_levels
from ..record import LogRecord
from .base import BaseFilter


class LevelFilter(BaseFilter):
    def __init__(
        self,
        *,
        exact_levels: list[LogLevelStructure] | str | None = None,
        exclude_levels: list[LogLevelStructure] | str | None = None,
    ) -> None:
        """_summary_

        Args:
            exact_levels (list[LogLevelStructure] | str, optional): support LogLevelName+ or +LogLevelName format. Defaults to None.
            exclude_levels (list[LogLevelStructure] | str, optional): support LogLevelName+ or +LogLevelName format. Defaults to None.
        """

        self.exact_levels = self._get_levels_list(exact_levels)
        self.exclude_levels = self._get_levels_list(exclude_levels)

    @staticmethod
    def _get_levels_list(
        levels: list[LogLevelStructure] | str | None,
    ) -> list[LogLevelStructure] | None:
        levels_list = None
        if isinstance(levels, list):
            levels_list = sorted(levels, key=lambda level: level.level)
        elif isinstance(levels, str):
            all_levels = list(get_all_levels().values())
            if levels.startswith("+"):
                level = get_all_levels().get(levels[1:])
                if level:
                    levels_list = all_levels[: all_levels.index(level)]
            elif levels.endswith("+"):
                level = get_all_levels().get(levels[:-1])
                if level:
                    levels_list = all_levels[all_levels.index(level) :]
            else:
                level = get_all_levels().get(levels, None)
                levels_list = [level] if level else None
        return levels_list

    async def filter(self, record: LogRecord) -> bool:
        return (
            self.exact_levels is None or record.level in self.exact_levels
        ) and (
            self.exclude_levels is None
            or record.level not in self.exclude_levels
        )
