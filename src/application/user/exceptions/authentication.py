from dataclasses import dataclass
from typing import ClassVar

from src.application.common.exceptions.base import ApplicationUserException


@dataclass(frozen=True)
class UserOrPasswordIsNotCorrectException(ApplicationUserException):
    """Raised when a user is not found in the database."""

    status: ClassVar[int] = 404

    def message(self):
        """User not found in the database."""
