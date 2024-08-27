from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizeUser:
    username: str
    password: str
