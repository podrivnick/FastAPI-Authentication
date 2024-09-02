from src.application.user.interfaces import UserAuthenticationRepo
from src.domain.user.entities.authenticated_user import AuthenticatedUser


class UserAuthenticationRepoMock(UserAuthenticationRepo):
    def __init__(self) -> None:
        self.users: dict[str, str] = {"koshka": "233sdad34"}

    async def authorize(self, auth_user: AuthenticatedUser) -> None:
        return f"{auth_user.key_authentication_token}:{auth_user.authentication_token}"

    async def verification_user(
        self,
        username: str,
        password: str,
    ) -> AuthenticatedUser:
        user = self.users[username]

        if not user:
            raise ValueError("Username")

        return AuthenticatedUser.create_authenticated_user(
            username=username,
            password=password,
        )
