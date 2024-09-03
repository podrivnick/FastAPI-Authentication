import re
from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException
from src.domain.common.value_objects.base import ValueObject


MAX_LENGTH_PASSWORD = 32
PASSWORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class BasePasswordException(ValueError, DomainException):
    password: str


class EmptyPasswordException(BasePasswordException):
    @property
    def title(self) -> str:
        return "Password can't be empty"


class TooLongPasswordException(BasePasswordException):
    @property
    def title(self) -> str:
        return f'Too long password "{self.password}"'


class WrongPasswordException(BasePasswordException):
    @property
    def title(self) -> str:
        return f'Wrong password format "{self.password}"'


@dataclass(frozen=True)
class Password(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if not self.exists():
            return

        if len(self.value) == 0:
            raise EmptyPasswordException(self.value)

        if len(self.value) > MAX_LENGTH_PASSWORD:
            raise TooLongPasswordException(self.value)

        if not PASSWORD_PATTERN.match(self.value):
            raise WrongPasswordException(self.value)

    def exists(self) -> bool:
        return self.value is not None
