from fastapi import APIRouter
from src.domain.user import events


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/create_user",
)
async def create_user(
    create_user: events.CreateUser,
) -> events.CreateUser:
    return events.CreateUser


@user_router.post(
    "/authorization",
)
async def login(
    user_login: events.AuthorizeUser,
) -> events.AuthorizeUser:
    return events.AuthorizeUser


@user_router.post(
    "/logout",
)
async def logout(
    logout_user: events.LogoutUser,
) -> events.LogoutUser:
    return events.LogoutUser
