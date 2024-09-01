from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from src.application.user.events import UserLogouted
from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user import value_objects as vo


@dataclass
class LogoutUser(AggregateRoot):
    auth_token: vo.AuthToken
    auth_key_token: str = field(default=None)

    @classmethod
    def create_logouted_user(
        cls,
        auth_token: vo.AuthToken,
    ) -> Self:
        auth_key_token = f"token:{auth_token.to_raw()}"

        user = cls(
            auth_token,
            auth_key_token,
        )
        user.record_event(
            UserLogouted(
                auth_token.to_raw(),
                auth_key_token,
            ),
        )
        return user
