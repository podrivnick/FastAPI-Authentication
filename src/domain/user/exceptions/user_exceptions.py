from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException


@dataclass(frozen=True)
class UserAlreadyExistsExceptions(DomainException):
    username: str | None

    @property
    def message(self) -> str:
        return f'User with username "{self.username}" already exists'
