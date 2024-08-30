from abc import (
    ABC,
    abstractclassmethod,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Protocol

from src.domain.user import value_objects
from src.domain.user.entities.user import User


@dataclass(frozen=True)
class UsersFilters(ABC):
    @abstractclassmethod
    async def get_user_by_username(self):
        pass


@dataclass(frozen=True)
class UsersAccounts(ABC):
    @abstractclassmethod
    async def authorize(self):
        pass

    @abstractclassmethod
    async def logout(self):
        pass


class UserRepo(Protocol):
    @abstractmethod
    async def add_user(self, user: User):
        raise NotImplementedError()

    @abstractmethod
    async def filter_by_username(self, username: value_objects.Username):
        raise NotImplementedError()
