from src.application.user import exceptions as exceptions_domain
from src.application.user.interfaces import UserLogoutedRepo
from src.domain.user.entities.logout_user import LogoutUser


class UserLogoutedRepoMock(UserLogoutedRepo):
    def __init__(self) -> None:
        self.token = "sfdsdfsdfs6df6sd"

    async def get_key_authentication_token(
        self,
        authentication_token: LogoutUser,
    ) -> None:
        if authentication_token.auth_token.to_raw() != self.token:
            raise exceptions_domain.TokenAuthorisationNotFoundException()
        return

    async def delete_authentication_token(
        self,
        authentication_token: LogoutUser,
    ) -> None:
        if authentication_token.auth_token.to_raw() != self.token:
            raise exceptions_domain.TokenAuthorisationNotDeletedException()
        return
