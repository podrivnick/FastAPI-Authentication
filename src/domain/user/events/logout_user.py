from dataclasses import dataclass

from src.application.common.base_command import Command


@dataclass(frozen=True)
class LogoutUserSchema(Command[str]):
    token: str

    def model_dump(self):
        return {
            "token": self.token,
        }
