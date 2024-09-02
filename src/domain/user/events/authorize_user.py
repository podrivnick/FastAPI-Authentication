from dataclasses import dataclass

from src.application.common.base_command import Command


@dataclass(frozen=True)
class AuthorizeUserSchema(Command[str]):
    username: str
    password: str

    def model_dump(self):
        return {
            "username": self.username,
            "password": self.password,
        }
