from dataclasses import dataclass

from src.application.common.exceptions.base import ApplicationUserException


@dataclass(frozen=True)
class UserAlreadyExistsExceptions(ApplicationUserException):
    """Raised when a username already exist in the database."""

    username: str | None

    @property
    def message(self) -> str:
        return f'User with username "{self.username}" already exists.'
