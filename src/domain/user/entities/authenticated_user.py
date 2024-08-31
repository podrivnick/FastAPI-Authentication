from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from src.application.user.events.user_created import UserAuthenticated
from src.domain.common.entities.aggregate_root import AggregateRoot


@dataclass
class AuthenticatedUser(AggregateRoot):
    username: str
    password: str
    key_authentication_token: str = field(default=None)
    authentication_token: str = field(default=None)

    @classmethod
    def create_authenticated_user(
        cls,
        username: str,
        password: str,
    ) -> Self:
        key_authentication_token, authentication_token = (
            cls.create_authentication_token()
        )
        authenticated_user = cls(
            username,
            password,
            key_authentication_token,
            authentication_token,
        )
        authenticated_user.record_event(
            UserAuthenticated(
                username,
                password,
                key_authentication_token,
                authentication_token,
            ),
        )
        return authenticated_user

    @staticmethod
    def create_authentication_token() -> tuple:
        from uuid import uuid4

        code = str(uuid4())
        key = f"token:{code}"

        return (key, code)
