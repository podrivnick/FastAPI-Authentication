from dataclasses import dataclass

from didiator import EventMediator
from src.application.common.base_command import CommandHandler
from src.application.user.interfaces.user import UserLogoutedRepo
from src.domain.user import value_objects as vo
from src.domain.user.entities.logout_user import LogoutUser
from src.domain.user.events.logout_user import LogoutUserSchema


@dataclass
class LogoutUserHandler(CommandHandler[LogoutUserSchema, str]):
    _user_repo: UserLogoutedRepo
    _mediator: EventMediator

    async def __call__(
        self,
        command: LogoutUserSchema,
    ) -> str:
        token: vo.AuthToken = vo.AuthToken(command.token)

        logouted_user: LogoutUser = LogoutUser.create_logouted_user(auth_token=token)

        await self._user_repo.get_key_authentication_token(logouted_user)
        await self._user_repo.delete_authentication_token(logouted_user)

        await self._mediator.publish(logouted_user.pull_events())

        return "User logged out successfully"
