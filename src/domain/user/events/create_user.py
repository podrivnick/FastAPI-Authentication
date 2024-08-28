from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True)
class CreateUser:
    username: str
    first_name: str
    last_name: str
    password: str
    middle_name: str = field(default=None)

    def model_dump(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "middle_name": self.middle_name,
        }
