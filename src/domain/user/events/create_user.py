from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True)
class CreateUser:
    username: str
    first_name: str
    last_name: str
    password: str
    middle_name: str = field(default=None)
