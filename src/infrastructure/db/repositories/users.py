from typing import (
    Any,
    Dict,
)

import asyncio_redis
from sqlalchemy import select
from src.application import (
    dto,
    interfaces,
)
from src.application.common import exceptions as exceptions_database
from src.application.user import exceptions as exceptions_domain
from src.domain.common.exceptions.base import BaseAppException
from src.domain.user import events
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
