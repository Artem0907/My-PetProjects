from asyncio import run as aiorun
from typing import NoReturn, Self, TypedDict

from aiofiles import open as aiopen
from openai import OpenAI


class DeepseekConfig(TypedDict):
    API_KEY: str
    BASE_URL: str
    MODEL_ID: str


class read_config:  # noqa: N801
    def __init__(
        self,
        file_name: str = "deepseek_openrouter",
        file_dir: str = "/".join(__file__.split("\\")[:-1]),
    ):
        self.file_name = f"{file_dir}/{file_name}.settings"

    async def read(
        self,
    ) -> DeepseekConfig:
        async with aiopen(self.file_name, encoding="utf-8") as config_file:
            configs: list[str] = await config_file.readlines()

        api_key = (
            next(config for config in configs if config.startswith("API_KEY"))
            .split("=")[-1]
            .strip()
            .strip('"')
        )
        base_url = (
            next(config for config in configs if config.startswith("BASE_URL"))
            .split("=")[-1]
            .strip()
            .strip('"')
        )
        model_id = (
            next(config for config in configs if config.startswith("MODEL_ID"))
            .split("=")[-1]
            .strip()
            .strip('"')
        )

        return DeepseekConfig(
            API_KEY=api_key, BASE_URL=base_url, MODEL_ID=model_id
        )

    async def get_config(self) -> Self:
        self.config = await self.read()
        self.API_KEY = self.config["API_KEY"]
        self.BASE_URL = self.config["BASE_URL"]
        self.MODEL_ID = self.config["MODEL_ID"]
        return self


async def deepseek(prompt: str) -> str | None:
    configs = await read_config().get_config()

    client = OpenAI(
        base_url=configs.BASE_URL,
        api_key=configs.API_KEY,
    )

    completion = client.chat.completions.create(
        extra_body={},
        model=configs.MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content


async def main() -> NoReturn:
    while True:
        prompt = input("prompt: ")
        print(await deepseek(prompt))  # noqa: T201


if __name__ == "__main__":
    try:
        aiorun(main())
    except InterruptedError:
        pass
