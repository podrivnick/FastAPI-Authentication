from dataclasses import dataclass

from src.application.common.base_command import CommandHandler
from src.application.user.interfaces.user import UserRepo
from src.domain.user import value_objects
from src.domain.user.entities.user import User
from src.domain.user.events.create_user import CreateUser


@dataclass
class CreateUserHandler(CommandHandler[CreateUser, str]):
    _user_repo: UserRepo

    async def __call__(
        self,
        command: CreateUser,
    ) -> str:
        username = value_objects.Username(command.username)
        full_name = value_objects.FullName(
            command.first_name,
            command.last_name,
            command.middle_name,
        )

        user = User.create_user(username, full_name)

        await self._user_repo.filter_by_username(username)
        await self._user_repo.add_user(user)

        return command.username
