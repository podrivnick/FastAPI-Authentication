import asyncio

from src.infrastructure.di.main import (
    setup_container,
    setup_db_factories,
    setup_mediator_factory,
)
from src.infrastructure.mediator import (
    init_mediator,
    setup_mediator,
)
from src.presentation.api.main import (
    init_api,
    run_api,
)


async def main() -> None:
    di_builder = setup_container()
    setup_mediator_factory(di_builder)
    setup_db_factories(di_builder)

    mediator = await di_builder.resolve(init_mediator)
    setup_mediator(mediator)

    app = init_api(mediator, di_builder, di_state, False)
    await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
