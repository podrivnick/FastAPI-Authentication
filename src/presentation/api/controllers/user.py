from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user import events
from src.infrastructure.db.main import get_async_session
from src.infrastructure.db.repositories.users import (
    UserAccount,
    UserReaderImpl,
)


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

    is_user_exist = await query.get_user_by_username(create_user.username)

    if is_user_exist:
        raise ValueError("User already exist")

    add_user = await query.create_user(create_user)

    return {"create_user": add_user}


@user_router.post(
    "/authorization",
    response_model=None,
)
async def login(
    user_login: events.AuthorizeUser,
    session: AsyncSession = Depends(get_async_session),
) -> events.AuthorizeUser:
    user_reader = UserReaderImpl(session)
    query = UserAccount(session)

    is_user_exist = await user_reader.get_user_by_username(user_login.username)
    if is_user_exist is None:
        raise ValueError("User doesn't exist")

    authorisation_code = await query.authorize(user_login=user_login)

    return authorisation_code


@user_router.post(
    "/logout",
)
async def logout(
    logout_user: events.LogoutUser,
) -> events.LogoutUser:
    return logout_user
