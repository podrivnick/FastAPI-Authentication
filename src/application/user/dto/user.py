from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class User(DTO):
    user_id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str = field(default=None)
