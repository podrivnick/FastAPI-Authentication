import re
from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException
from src.domain.common.value_objects.base import ValueObject


MAX_LENGTH_PASSWORD = 32
PASSWORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class BaseExceptonPassword(ValueError, DomainException):
    password: str


class EmptyPasswordError(BaseExceptonPassword):
    @property
    def title(self) -> str:
        return "Password can't be empty"


class TooLongPasswordError(BaseExceptonPassword):
    @property
    def title(self) -> str:
        return f'Too long password "{self.password}"'


class WrongPasswordFormatError(BaseExceptonPassword):
    @property
    def title(self) -> str:
        return f'Wrong password format "{self.password}"'


@dataclass(frozen=True)
class Password(ValueObject[str | None]):
    value: str | None

    def _validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyPasswordError(self.value)

        if len(self.value) > MAX_LENGTH_PASSWORD:
            raise TooLongPasswordError(self.value)

        if not PASSWORD_PATTERN.match(self.value):
            raise WrongPasswordFormatError(self.value)

    def exists(self) -> bool:
        return self.value is not None
