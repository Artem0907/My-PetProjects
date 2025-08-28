from argparse import ArgumentParser, Namespace
from asyncio import run as _async_run
from contextlib import suppress
from json import dumps
from pathlib import Path

from aiofiles import open as _aio_open
from aiofiles.os import listdir
from aiofiles.os import mkdir as _create_folder

type _T = dict[str, list[str | dict]]


class ObsidianTools:
    def __init__(self, args: Namespace):
        self.args = dict(args._get_kwargs())

        self.set_path: Path | None = (
            self.args["set_path"][0]
            if self.args.get("set_path")
            and isinstance(self.args["set_path"][0], Path)
            else None
        )
        self.create_note: str | None = (
            self.args["create_note"][0]
            if self.args.get("create_note")
            and isinstance(self.args["create_note"][0], str)
            else None
        )
        self.create_folder: str | None = (
            self.args["create_folder"][0]
            if self.args.get("create_folder")
            and isinstance(self.args["create_folder"][0], str)
            else None
        )
        self.read_note: str | None = (
            self.args["read_note"][0]
            if self.args.get("read_note")
            and isinstance(self.args["read_note"][0], str)
            else None
        )

    async def __call__(self, settings_path: Path) -> None:
        if (
            not settings_path.exists()
            or not settings_path.is_file()
            or (
                settings_path.suffix != ".settings"
                and settings_path.name != ".settings"
            )
        ):
            raise ValueError("enter valid path")

        async with _aio_open(settings_path) as fb:
            read_data = {
                string.split("=")[0]
                .replace('"', "")
                .strip()
                .lower(): (
                    string.split("=")[1].replace('"', "").strip()
                    if string.split("=")[1].replace('"', "").strip() != "None"
                    else None
                )
                for string in await fb.readlines()
            }
        async with _aio_open(settings_path, "wb") as fb:
            data: dict[str, str] = {}
            data["notes_dir_path"] = str(
                self.set_path or read_data.get("notes_dir_path")
            ).replace("\\", "/")
            write_data = (f'{el[0].upper()} = "{el[1]}"' for el in data.items())
            await fb.write("\n".join(write_data).encode("utf-8"))

        self.notes_path = (
            Path(data["notes_dir_path"])
            if data["notes_dir_path"] != "None"
            else Path(__file__).parent
        )

        if self.create_folder:
            with suppress(FileExistsError):
                await _create_folder(self.notes_path / self.create_folder)
        if self.create_note:
            with suppress(FileExistsError):
                async with _aio_open((self.notes_path / self.create_note), "x"):
                    ...
        if self.read_note:
            if (self.notes_path / self.read_note).exists() and (
                self.notes_path / self.read_note
            ).suffix == ".md":
                async with _aio_open(
                    (self.notes_path / self.read_note), "rb"
                ) as fb:
                    print((await fb.read()).decode("utf-8"))  # noqa: T201

        else:

            async def list_dir(
                dir_path: str,
            ) -> _T:
                returning: _T = {}
                paths = list(
                    filter(
                        lambda path: path
                        not in [
                            ".gitignore",
                            ".obsidian",
                            ".ropeproject",
                            ".trash",
                        ],
                        await listdir(dir_path),
                    )
                )
                returning[Path(dir_path).name] = []
                for path in paths:
                    full_path = str(Path(dir_path) / path)
                    returning[Path(dir_path).name].append(
                        await list_dir(full_path)
                        if Path(full_path).is_dir()
                        else Path(full_path).name
                    )
                return dict(sorted(returning.items()))

            print(  # noqa: T201
                dumps(
                    await list_dir(str(self.notes_path)),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )


parser = ArgumentParser()
parser.add_argument(
    "--set-path",
    "-sp",
    type=lambda string: (Path(string) if Path(string).suffix == "" else False),
    nargs=1,
    default=None,
    metavar="DIR_PATH",
    help="path to notes",
)
parser.add_argument(
    "--create-note",
    "-cn",
    type=lambda string: (string if Path(string).suffix == ".md" else False),
    nargs=1,
    default=None,
    metavar="FILE_PATH",
    help="path to new note",
)
parser.add_argument(
    "--create-folder",
    "-cf",
    type=lambda string: (string if Path(string).suffix == "" else False),
    nargs=1,
    default=None,
    metavar="DIR_PATH",
    help="path to new folder",
)
parser.add_argument(
    "--read-note",
    "-rn",
    type=lambda string: (string if Path(string).suffix == ".md" else False),
    nargs=1,
    default=None,
    metavar="FILE_PATH",
    help="path to note with read",
)

_async_run(
    ObsidianTools(parser.parse_args())(Path(__file__).parent / ".settings")
)
