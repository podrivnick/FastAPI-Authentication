from sqlalchemy import select
from src.application.user import dto
from src.application.user.interfaces import UsersFilters
from src.infrastructure.db.converters import convert_db_model_to_active_user_dto
from src.infrastructure.db.models.user import User
from src.infrastructure.db.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo, UsersFilters):
    async def get_user_by_username(
        self,
        username: str,
    ) -> dto.User:
        user: User | None = await self._session.scalar(
            select(User).where(User.username == username),
        )
        if user is None:
            raise ValueError(username)

        return convert_db_model_to_active_user_dto(user)
