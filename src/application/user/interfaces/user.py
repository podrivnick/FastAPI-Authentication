from abc import abstractmethod
from typing import Protocol

from src.application.user import dto
from src.domain.user.entities.authenticated_user import AuthenticatedUser
from src.domain.user.entities.logout_user import LogoutUser
from src.domain.user.entities.user import User


class UserRepo(Protocol):
    @abstractmethod
    async def add_user(self, user: User) -> dto.User:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_username(self, user: User) -> dto.User:
        raise NotImplementedError()


class UserAuthenticationRepo(Protocol):
    @abstractmethod
    async def authorize(self, user_auth: AuthenticatedUser) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def verification_user(
        self,
        user_auth: AuthenticatedUser,
    ) -> AuthenticatedUser:
        raise NotImplementedError()


class UserLogoutedRepo(Protocol):
    @abstractmethod
    async def get_key_authentication_token(self, auth_token: LogoutUser) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_authentication_token(
        self,
        auth_token: LogoutUser,
    ) -> AuthenticatedUser:
        raise NotImplementedError()
