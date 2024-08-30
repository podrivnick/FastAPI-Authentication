from abc import (
    ABC,
    abstractclassmethod,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Protocol

from src.application.user import dto
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
    async def add_user(self, user: User) -> dto.User:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_username(self, user: User) -> dto.User:
        raise NotImplementedError()
