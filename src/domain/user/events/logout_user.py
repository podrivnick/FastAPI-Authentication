from dataclasses import dataclass


@dataclass(frozen=True)
class LogoutUser:
    username: str