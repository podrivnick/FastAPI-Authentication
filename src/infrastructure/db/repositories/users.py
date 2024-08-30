from typing import (
    Any,
    Dict,
    NoReturn,
)

import asyncio_redis
from sqlalchemy import select
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
)
from src.application.common import (
    exceptions,
    exceptions as exceptions_database,
)
from src.application.user import (
    dto,
    exceptions as exceptions_domain,
    interfaces,
)
from src.application.user.exceptions import UserAlreadyExistsExceptions
from src.domain.common.exceptions.base import BaseAppException
from src.domain.user import (
    entities,
    events,
)
from src.infrastructure.db.converters import (
    convert_db_model_to_user_entity,
    convert_user_entity_to_db_model,
)
from src.infrastructure.db.exceptions_mapper import exceptions_mapper
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


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


class UserReaderImpl(SQLAlchemyRepo, interfaces.UsersFilters):
    async def get_user_by_username(
        self,
        filtering_data: Dict[str, Any],
    ) -> dto.User:
        stmt = select(User).filter_by(**filtering_data)
        user = await self._session.execute(stmt)

        result_user = user.scalars().first()

        return result_user

    async def create_user(
        self,
        create_user: events.CreateUser,
    ) -> dto.User:
        user = User(
            username=create_user.username,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            middle_name=create_user.middle_name,
            password=create_user.password,
        )
        self._session.add(user)

        try:
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        return user


class UserRepoAlchemyImpl(SQLAlchemyRepo, interfaces.UserRepo):
    @exceptions_mapper
    async def add_user(
        self,
        create_user: entities.User,
    ) -> dto.User:
        user_model = convert_user_entity_to_db_model(create_user)
        user_model = User(
            username=create_user.username,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            middle_name=create_user.middle_name,
            password=create_user.password,
        )
        self._session.add(user_model)

        try:
            await self._session.flush((user_model,))
        except IntegrityError as exception:
            self._parse_error(exception, create_user)

    @exceptions_mapper
    async def get_user_by_username(
        self,
        user: entities.User,
    ) -> dto.User:
        stmt = select(User).filter_by(username=user.username)

        await self._session.execute(stmt)

        try:
            user_filtered = user.scalars().first()
        except IntegrityError as exception:
            self._parse_error(exception, user)

        return convert_db_model_to_user_entity(user_filtered)

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "uq_users_username":
                raise UserAlreadyExistsExceptions(str(user.username)) from err
            case _:
                raise exceptions.RepoException from err
