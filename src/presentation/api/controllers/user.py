from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user import events
from src.infrastructure.db.main import get_async_session
from src.infrastructure.db.repositories.users import UserReaderImpl


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/create_user",
    response_model=None,
)
async def create_user(
    create_user: events.CreateUser,
    session: AsyncSession = Depends(get_async_session),
) -> events.CreateUser:
    query = UserReaderImpl(session)

    await query.get_user_by_username(create_user.username)
    add_user = await query.create_user(create_user)

    return {"create_user": add_user}


@user_router.post(
    "/authorization",
)
async def login(
    user_login: events.AuthorizeUser,
) -> events.AuthorizeUser:
    return user_login


@user_router.post(
    "/logout",
)
async def logout(
    logout_user: events.LogoutUser,
) -> events.LogoutUser:
    return logout_user
