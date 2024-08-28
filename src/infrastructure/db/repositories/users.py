from sqlalchemy import select
from src.application import (
    dto,
    interfaces,
)
from src.domain.user import events
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo, interfaces.UsersFilters):
    async def get_user_by_username(
        self,
        username: str,
    ) -> dto.User:
        user: User | None = await self._session.scalar(
            select(User).where(User.username == username),
        )
        if user:
            raise ValueError(username)

        return username

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
