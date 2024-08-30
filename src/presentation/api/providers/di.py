from collections.abc import AsyncGenerator

from fastapi import Depends
from punq import Container
from src.infrastructure.di import DiScope


def get_di_container() -> Container:
    raise NotImplementedError


class StateProvider:
    def __init__(self, di_container: Container | None = None) -> None:
        self._di_container = di_container

    async def build(
        self,
        di_container: Container = Depends(get_di_container),
    ) -> AsyncGenerator[Container, None]:
        async with di_container.scope(DiScope.REQUEST) as di_state:
            yield di_state
