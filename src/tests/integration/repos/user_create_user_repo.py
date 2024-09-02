from src.application.user.interfaces import UserRepo
from src.domain.user import entities
from src.domain.user.value_objects import UserName


class UserRepoMock(UserRepo):
    def __init__(self) -> None:
        self.users: dict[UserName, entities.User] = {}

    async def add_user(self, user: entities.User) -> None:
        self.users[user.username] = user

    async def get_user_by_username(self, user_entity: entities.User) -> set[UserName]:
        usernames = {user.username for user in self.users.values()}
        return usernames
