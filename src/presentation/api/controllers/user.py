from fastapi import APIRouter
from src.domain.user.events.create_user import CreateUser


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "create_user",
)
async def create_user(
    create_user: CreateUser,
):
    return CreateUser


# @user_router.post(
#     "authorization",
#     status_code=status.HTTP_201_CREATED,
# )
# async def login():
#     return


# @user_router.post(
#     "logout",
#     status_code=status.HTTP_201_CREATED,
# )
# async def logout():
#     return
