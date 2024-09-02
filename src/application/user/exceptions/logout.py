from dataclasses import dataclass
from typing import ClassVar

from src.application.common.exceptions.base import ApplicationUserException


@dataclass(eq=False)
class TokenAuthorisationNotFoundException(ApplicationUserException):
    """Raised when a token is not found in the database."""

    status: ClassVar[int] = 404

    @property
    def message(self) -> str:
        return "Token not found in the database."


@dataclass(eq=False)
class TokenAuthorisationNotDeletedException(ApplicationUserException):
    """Raised when a token is not found in the database."""

    status: ClassVar[int] = 404

    @property
    def message(self) -> str:
        return "Token not deleted."
