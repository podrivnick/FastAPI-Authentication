from src.domain.user import entities
from src.infrastructure.db import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        middle_name=user.full_name.middle_name,
    )


def convert_db_model_to_user_entity(
    user: models.User,
) -> entities.User:
    return entities.User(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
    )
