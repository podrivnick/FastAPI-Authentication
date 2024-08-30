from dataclasses import (
    dataclass,
    field,
)

from src.domain.common.events.base import Event


@dataclass(frozen=True)
class UserCreated(Event):
    username: str
    first_name: str
    last_name: str
    password: str
    middle_name: str = field(default=None)
