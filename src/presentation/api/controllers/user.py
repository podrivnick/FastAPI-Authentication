from fastapi import (
    APIRouter,
    status,
)


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "create_user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user():
    return


@user_router.post(
    "authorization",
    status_code=status.HTTP_201_CREATED,
)
async def login():
    return


@user_router.post(
    "logout",
    status_code=status.HTTP_201_CREATED,
)
async def logout():
    return
