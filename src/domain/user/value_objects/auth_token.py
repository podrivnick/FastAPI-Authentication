from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException
from src.domain.common.value_objects.base import ValueObject


MAX_AUTH_TOKEN_LENGTH = 32


@dataclass(eq=False)
class BaseAuthTokenException(ValueError, DomainException):
    @property
    def message(self) -> str:
        return "Authentication token is invalid"


class AuthTokenIsEmptyException(BaseAuthTokenException):
    @property
    def message(self) -> str:
        return "Authentication token can't be empty"


class AuthTokenTooLongException(BaseAuthTokenException):
    @property
    def message(self) -> str:
        return "Authentication token is too long"


@dataclass(frozen=True)
class AuthToken(ValueObject[str | None]):
    value: str | None

    def _validate(self) -> None:
        if len(self.value) == 0:
            raise AuthTokenIsEmptyException()
        if len(self.value) > MAX_AUTH_TOKEN_LENGTH:
            raise AuthTokenTooLongException()

    def __str__(self) -> str:
        if self.value:
            return f"{self.value}"
