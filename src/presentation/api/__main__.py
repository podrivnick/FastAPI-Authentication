import asyncio

from presentation.api.config import APIConfig
from presentation.api.main import (
    init_api,
    run_api,
)

from .config import DEBUG


async def main() -> None:
    app = init_api(DEBUG)

    await run_api(app, APIConfig)


if __name__ == "__main__":
    asyncio.run(main())
