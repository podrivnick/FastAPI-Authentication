from abc import (
    ABC,
    abstractclassmethod,
)
from dataclasses import dataclass


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
