from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.application import dto
from src.domain.user import events
from src.domain.user.exceptions.user_exceptions import UserAlreadyExistsExceptions
from src.domain.user.value_objects.username import (
    EmptyUsernameError,
    TooLongUsernameError,
    WrongUsernameFormatError,
)
from src.infrastructure.db.main import get_async_session
from src.infrastructure.db.repositories.users import (
    UserAccount,
    UserReaderImpl,
)
from src.presentation.api.controllers.responses.base import (
    FailureResponse,
    SuccessResponse,
)


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/create_user",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": FailureResponse[
                TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[UserAlreadyExistsExceptions],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user: events.CreateUser,
    session: AsyncSession = Depends(get_async_session),
) -> events.CreateUser:
    query = UserReaderImpl(session)

    is_user_exist = await query.get_user_by_username(create_user.model_dump())

    if is_user_exist:
        raise UserAlreadyExistsExceptions(create_user.model_dump()["username"])

    add_user = await query.create_user(create_user)

    return SuccessResponse(result=add_user)


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

    is_user_exist = await user_reader.get_user_by_username(user_login.model_dump())
    if is_user_exist is None:
        raise ValueError("User doesn't exist")

    authorisation_code = await query.authorize(user_login=user_login)

    return authorisation_code


@user_router.delete(
    "/logout",
    response_model=None,
)
async def logout(
    logout_user: events.LogoutUser,
    session: AsyncSession = Depends(get_async_session),
) -> events.LogoutUser:
    query = UserAccount(session)

    is_deleted = await query.logout(token_schema=logout_user)
    if not is_deleted:
        raise ValueError("Token doesn't exist")

    return {
        "message": "User logged out successfully",
        "logout_user": logout_user,
    }
