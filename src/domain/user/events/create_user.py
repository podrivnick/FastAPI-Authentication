from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(frozen=True)
class CreateUser:
    user_id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str = field(default=None)
