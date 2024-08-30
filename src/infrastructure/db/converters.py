from src.domain.user import (
    entities,
    value_objects as vo,
)
from src.infrastructure.db import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        password=user.password,  # TODO: hash password before storing
        middle_name=user.full_name.middle_name,
    )


def convert_db_model_to_user_entity(
    user: models.User,
) -> entities.User:
    full_name = vo.FullName(
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )

    return entities.User(
        username=vo.Username(user.username),
        full_name=full_name,
    )
