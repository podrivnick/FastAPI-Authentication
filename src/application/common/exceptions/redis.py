from dataclasses import dataclass

from src.domain.common.exceptions.base import BaseAppException


@dataclass(frozen=True)
class RedisConnectionError(BaseAppException):
    """Raised when the connection to Redis fails."""

    @property
    def message(self) -> str:
        return "Failed to connect to Redis"