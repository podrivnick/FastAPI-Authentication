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


@dataclass(frozen=True)
class UserAuthenticated(Event):
    username: str
    password: str
    key_authintication_token: str
    authentication_token: str
