import uuid
from dataclasses import (
    dataclass,
    field,
)

from src.domain.common.entities import Entity


@dataclass(frozen=True)
class User(Entity):
    user_id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str = field(default=None, init=False)

    @classmethod
    def create_user(
        cls,
    ) -> "User":
        return cls(
            user_id=uuid.uuid4(),
            username=None,
            first_name="",
            last_name="",
        )
