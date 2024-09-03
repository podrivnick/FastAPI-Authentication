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
    EmptyUsernameException,
    TooLongUsernameException,
    WrongUsernameFormatException,
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
                TooLongUsernameException
                | EmptyUsernameException
                | WrongUsernameFormatException
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[exceptions.UserAlreadyExistsExceptions],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: events.CreateUserSchema,
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
                TooLongUsernameException
                | EmptyUsernameException
                | WrongUsernameFormatException
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": FailureResponse[exceptions.UserOrPasswordIsNotCorrectException],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def login(
    user_login: events.AuthorizeUserSchema,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> SuccessResponse[str]:
    """Зайти в аккаунт."""

    authorisation_token = await mediator.send(user_login)

    return SuccessResponse(result=authorisation_token)


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
    logout_user: events.LogoutUserSchema,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> SuccessResponse[str]:
    """Выйти с аккаунта."""
    user_logout = await mediator.send(logout_user)

    return SuccessResponse(result=user_logout)
