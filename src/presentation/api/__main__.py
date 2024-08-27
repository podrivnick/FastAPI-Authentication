import asyncio

from src.presentation.api.config import APIConfig
from src.presentation.api.main import (
    init_api,
    run_api,
)
from src.settings.config import DEBUG


async def main() -> None:
    app = await init_api(DEBUG)

    await run_api(app, APIConfig)


if __name__ == "__main__":
    asyncio.run(main())
