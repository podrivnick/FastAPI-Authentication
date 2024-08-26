from uuid import UUID

from application.user import dto
from application.user.exceptions import (
    UserIdNotExistError,
    UsernameNotExistError,
)
from application.user.interfaces.persistence import (
    GetUsersFilters,
    UserReader,
)
from infrastructure.db.converters import (
    convert_db_model_to_active_user_dto,
    convert_db_model_to_user_dto,
)
from infrastructure.db.exception_mapper import exception_mapper
from infrastructure.db.models.user import User
from infrastructure.db.repositories.base import SQLAlchemyRepo
from sqlalchemy import select


class UserReaderImpl(SQLAlchemyRepo, UserReader):
    @exception_mapper
    async def get_user_by_id(self, user_id: UUID) -> dto.UserDTOs:
        user: User | None = await self._session.get(User, user_id)
        if user is None:
            raise UserIdNotExistError(user_id)

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_username(self, username: str) -> dto.User:
        user: User | None = await self._session.scalar(
            select(User).where(User.username == username),
        )
        if user is None:
            raise UsernameNotExistError(username)

        return convert_db_model_to_active_user_dto(user)

    @exception_mapper
    async def get_users(self, filters: GetUsersFilters) -> dto.Users:
        users = await GetUsersFilters.filter(User.username == self.username)

        return dto.Users(data=users)
