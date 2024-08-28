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
        print("Waiting for redis...")
        connection = await asyncio_redis.Connection.create(host="redis", port=6379)

        key = f"token:{code}"
        await connection.set(key, code)

        connection.close()

        return code

    async def logout(
        self,
        token_schema: events.LogoutUser,
    ) -> bool:
        is_deleted = False

        print("Waiting for redis...")

        try:
            connection = await asyncio_redis.Connection.create(host="redis", port=6379)
            print(f"Looking for token: {token_schema.token}")

            key = f"token:{token_schema.token}"
            is_token_exist = await connection.get(key)

            if is_token_exist:
                print("Deleting token...")
                await connection.delete([key])
                is_deleted = True
            else:
                print("Token doesn't exist")
        except Exception as e:
            print(f"Error interacting with Redis: {e}")
            raise
        finally:
            connection.close()

        return is_deleted


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
