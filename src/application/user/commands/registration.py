from dataclasses import dataclass

from didiator import EventMediator
from src.application.common.base_command import CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.user import UserRepo
from src.domain.user import value_objects
from src.domain.user.entities.user import User
from src.domain.user.events.create_user import CreateUser


@dataclass
class CreateUserHandler(CommandHandler[CreateUser, str]):
    _user_repo: UserRepo
    _uow: UnitOfWork
    _mediator: EventMediator

    async def __call__(
        self,
        command: CreateUser,
    ) -> str:
        username = value_objects.UserName(command.username)
        full_name = value_objects.FullName(
            command.first_name,
            command.last_name,
            command.middle_name,
        )
        password = value_objects.Password(command.password)

        user = User.create_user(username, full_name, password)

        await self._user_repo.get_user_by_username(user)
        await self._user_repo.add_user(user)

        await self._mediator.publish(user.pull_events())

        await self._uow.commit()

        return command.username
