from dataclasses import dataclass
from typing import Self

from src.application.user.events.user_created import UserCreated
from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user import value_objects


@dataclass(frozen=True)
class User(AggregateRoot):
    username: value_objects.UserName
    full_name: value_objects.FullName

    @classmethod
    def create_user(
        cls,
        username: value_objects.UserName,
        full_name: value_objects.FullName,
    ) -> Self:
        user = cls(username, full_name)
        user.record_event(
            UserCreated(
                username.to_raw(),
                full_name.first_name,
                full_name.last_name,
                full_name.middle_name,
            ),
        )
        return user
