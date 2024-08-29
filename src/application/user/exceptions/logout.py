from dataclasses import dataclass
from typing import ClassVar

from src.application.common.exceptions.base import ApplicationUserException


@dataclass(frozen=True)
class TokenAuthorisationNotFoundException(ApplicationUserException):
    """Raised when a token is not found in the database."""

    status: ClassVar[int] = 404

    @property
    def message(self) -> str:
        """Token not found in the database."""


@dataclass(frozen=True)
class TokenAuthorisationNotDeletedException(ApplicationUserException):
    """Raised when a token is not found in the database."""

    status: ClassVar[int] = 404

    @property
    def message(self) -> str:
        """Token not deleted."""
