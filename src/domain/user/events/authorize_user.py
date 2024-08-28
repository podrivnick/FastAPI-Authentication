from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizeUser:
    username: str
    password: str

    def model_dump(self):
        return {
            "username": self.username,
            "password": self.password,
        }
