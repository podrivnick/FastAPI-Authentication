from dataclasses import dataclass
from typing import Self

from src.application.user.events import UserCreated
from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user import value_objects


@dataclass
class User(AggregateRoot):
    username: value_objects.UserName
    full_name: value_objects.FullName
    password: value_objects.Password

    @classmethod
    def create_user(
        cls,
        username: value_objects.UserName,
        full_name: value_objects.FullName,
        password: value_objects.Password,
    ) -> Self:
        user = cls(username, full_name, password)
        user.record_event(
            UserCreated(
                username.to_raw(),
                password.to_raw(),
                full_name.first_name,
                full_name.last_name,
                full_name.middle_name,
            ),
        )
        return user
