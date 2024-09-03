import re
from dataclasses import dataclass

from src.domain.common.exceptions.base import DomainException
from src.domain.common.value_objects.base import ValueObject


MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class BaseExceptonUsername(ValueError, DomainException):
    username: str


class EmptyUsernameError(BaseExceptonUsername):
    @property
    def message(self) -> str:
        return "Username can't be empty"


class TooLongUsernameError(BaseExceptonUsername):
    @property
    def message(self) -> str:
        return f'Too long username "{self.username}"'


class WrongUsernameFormatError(BaseExceptonUsername):
    @property
    def message(self) -> str:
        return f'Wrong username format "{self.username}"'


@dataclass(frozen=True)
class UserName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyUsernameError(self.value)

        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsernameError(self.value)

        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormatError(self.value)

    def exists(self) -> bool:
        return self.value is not None
