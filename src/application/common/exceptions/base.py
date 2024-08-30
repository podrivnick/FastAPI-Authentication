from dataclasses import dataclass

from src.domain.common.exceptions.base import BaseAppException


@dataclass(eq=False)
class ApplicationUserException(BaseAppException):
    """Base class for application user exceptions."""

    @property
    def message(self) -> str:
        return "An error occurred while handling the user's request"


@dataclass(eq=False)
class RepoException(ApplicationUserException):
    """Base class for unexpected repository exceptions."""

    @property
    def message(self) -> str:
        return "An unexpected error occurred while interacting with the repository"


@dataclass(eq=False)
class CommitError(ApplicationUserException):
    """Raised when a commit operation fails."""

    @property
    def message(self) -> str:
        return "Failed to commit session"


@dataclass(eq=False)
class RollbackError(ApplicationUserException):
    """Raised when a rollback operation fails."""

    @property
    def message(self) -> str:
        return "Failed to rollback session"
