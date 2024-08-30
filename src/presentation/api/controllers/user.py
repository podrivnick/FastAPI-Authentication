from typing import Annotated

from didiator import Mediator
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from src.application.user import (
    dto,
    exceptions,
)
from src.domain.user import events
from src.domain.user.value_objects.username import (
    EmptyUsernameError,
    TooLongUsernameError,
    WrongUsernameFormatError,
)
from src.infrastructure.db.repositories.users import (
    UserAccount,
    UserReaderImpl,
)
from src.presentation.api.controllers.responses.base import (
    FailureResponse,
    SuccessResponse,
)
from src.presentation.api.providers.stub import Stub


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/create_user",
    description="Эндпоинт Регистрирует пользователя, если пользователь уже есть => Error 409",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": FailureResponse[
                TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[exceptions.UserAlreadyExistsExceptions],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: events.CreateUser,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> SuccessResponse[dto.User]:
    """Зарегистрировать аккаунт."""

    user_username = await mediator.send(create_user_command)

    return SuccessResponse(result=user_username)


@user_router.post(
    "/authorization",
    description="Эндпоинт Аутентифицирует и Авторизирует пользователя, если пользователь отсутствует или пароль неверный => Error 409",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": FailureResponse[
                TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[exceptions.UserOrPasswordIsNotCorrectException],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def login(
    user_login: events.AuthorizeUser,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> SuccessResponse:
    """Зайти в аккаунт."""
    session = ""
    user_reader = UserReaderImpl(session)
    query = UserAccount(session)

    is_user_exist = await user_reader.get_user_by_username(user_login.model_dump())
    if is_user_exist is None:
        raise exceptions.UserOrPasswordIsNotCorrectException()

    authorisation_code = await query.authorize(user_login=user_login)

    return SuccessResponse(result=authorisation_code)


@user_router.delete(
    "/logout",
    description="Эндпоинт Удаляет Токен Авторизации у пользователя, если токен не найден или не удалён => Error 409",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[
                exceptions.TokenAuthorisationNotDeletedException
                | exceptions.TokenAuthorisationNotFoundException
            ],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def logout(
    logout_user: events.LogoutUser,
) -> events.LogoutUser:
    """Выйти с аккаунта."""
    session = ""
    query = UserAccount(session)

    is_deleted = await query.logout(token_schema=logout_user)

    return SuccessResponse(result=is_deleted)
