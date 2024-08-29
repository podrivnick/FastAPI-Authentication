from dataclasses import dataclass

from src.domain.common.exceptions.base import BaseAppException


@dataclass(frozen=True)
class ApplicationUserException(BaseAppException):
    """Base class for application user exceptions."""

    @property
    def message(self) -> str:
        return "An error occurred while handling the user's request"
