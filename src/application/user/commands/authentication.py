from dataclasses import dataclass

from didiator import EventMediator
from src.application.common.base_command import CommandHandler
from src.application.user.interfaces.user import UserAuthenticationRepo
from src.domain.user import (
    events,
    value_objects,
)
from src.domain.user.entities.authenticated_user import AuthenticatedUser


@dataclass
class AuthorizeUserHandler(CommandHandler[events.AuthorizeUser, str]):
    _user_repo: UserAuthenticationRepo
    _mediator: EventMediator

    async def __call__(
        self,
        command: events.AuthorizeUser,
    ) -> str:
        username = value_objects.UserName(command.username)
        password = value_objects.Password(command.password)

        authenticated_user: AuthenticatedUser = await self._user_repo.verification_user(
            username=username.to_raw(),
            password=password.to_raw(),
        )

        await self._user_repo.authorize(authenticated_user)
        await self._mediator.publish(authenticated_user.pull_events())

        return str(authenticated_user.authentication_token)
