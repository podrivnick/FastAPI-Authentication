from typing import Any

from didiator import Mediator
from fastapi import Depends
from punq import Container
from src.infrastructure.mediator import get_mediator

from .di import get_di_container


class MediatorProvider:
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def build(
        self,
        di_container: Container = Depends(get_di_container),
    ) -> Mediator:
        di_state = di_container.scope()  # Получаем состояние контейнера
        di_values: dict[Any, Any] = {Container: di_state}
        mediator = self._mediator.bind(di_state=di_state, di_values=di_values)
        di_values[get_mediator] = mediator
        return mediator
