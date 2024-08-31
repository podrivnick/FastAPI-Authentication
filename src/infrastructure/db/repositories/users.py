from typing import NoReturn

import asyncio_redis
from sqlalchemy import select
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
)
from src.application.common import exceptions as exceptions_database
from src.application.user import (
    dto,
    exceptions as exceptions_domain,
    interfaces,
)
from src.domain.common.exceptions.base import BaseAppException
from src.domain.user import (
    entities,
    events,
)
from src.domain.user.entities.authenticated_user import AuthenticatedUser
from src.infrastructure.db.converters import convert_user_entity_to_db_model
from src.infrastructure.db.exception_mapper import exception_mapper
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserAuthenticationRepoAlchemyImpl(
    SQLAlchemyRepo,
    interfaces.UserAuthenticationRepo,
):
    @exception_mapper
    async def authorize(self, user_auth: AuthenticatedUser) -> None:
        connection_redis = self._connection_redis

        if not connection_redis:
            raise exceptions_database.RedisConnectionError()

        await connection_redis.set(
            user_auth.key_authentication_token,
            user_auth.authentication_token,
        )

        connection_redis.close()

    @exception_mapper
    async def verification_user(
        self,
        username: str,
        password: str,
    ) -> AuthenticatedUser:
        user: User | None = await self._session.scalar(
            select(User).where(
                User.username == username,
                User.password == password,
            ),
        )

        if not user:
            raise exceptions_domain.UserOrPasswordIsNotCorrectException()

        return AuthenticatedUser.create_authenticated_user(
            username=username,
            password=password,
        )


class UserAccount(SQLAlchemyRepo, interfaces.UsersAccounts):
    async def authorize(
        self,
        user_login: events.AuthorizeUser,
    ) -> str:
        from uuid import uuid4

        code = str(uuid4())

        connection = await self._get_redis_connection()
        if not connection:
            raise exceptions_database.RedisConnectionError()

        key = f"token:{code}"
        await connection.set(key, code)

        connection.close()

        return code

    async def logout(
        self,
        token_schema: events.LogoutUser,
    ) -> bool:
        key = f"token:{token_schema.token}"

        connection = await self._get_redis_connection()
        if not connection:
            raise exceptions_database.RedisConnectionError()

        try:
            is_token_exist = await connection.get(key)
            if not is_token_exist:
                raise exceptions_domain.TokenAuthorisationNotFoundException()

            delete_token = await connection.delete([key])
            if not delete_token:
                raise exceptions_domain.TokenAuthorisationNotDeletedException()

            return True
        except BaseAppException as exception:
            print(exception.message)
            return False
        finally:
            connection.close()

    async def _get_redis_connection(self):
        try:
            return await asyncio_redis.Connection.create(host="redis", port=6379)
        except Exception:
            return None


class UserRepoAlchemyImpl(SQLAlchemyRepo, interfaces.UserRepo):
    @exception_mapper
    async def add_user(
        self,
        create_user: entities.User,
    ) -> dto.User:
        user_model = convert_user_entity_to_db_model(create_user)
        self._session.add(user_model)

        try:
            await self._session.flush((user_model,))
        except IntegrityError as exception:
            self._parse_error(exception, create_user)

    @exception_mapper
    async def get_user_by_username(
        self,
        user: entities.User,
    ) -> dto.User:
        username = user.username.to_raw()  # type: ignore  # TODO: fix mypy error
        user: entities.User | None = await self._session.scalar(
            select(User).where(User.username == username),
        )

        if user:
            raise exceptions_domain.UserAlreadyExistsExceptions(username)

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "uq_users_username":
                raise exceptions_domain.UserAlreadyExistsExceptions(
                    str(user.username),
                ) from err
            case _:
                raise exceptions_database.RepoException from err
