import pytest
from src.application.user.commands.registration import CreateUserHandler
from src.domain.user import value_objects as vo
from src.domain.user.events.create_user import CreateUserSchema
from src.tests.integration.repos.user_create_user_repo import UserRepoMock
from src.tests.mock.event_mediator import EventMediatorMock
from src.tests.mock.uow import UnitOfWorkMock


@pytest.mark.asyncio
async def test_create_user_handler(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = CreateUserHandler(user_repo, uow, event_mediator)

    username = vo.UserName("koshka")

    command = CreateUserSchema(
        username="koshka",
        first_name="ghan",
        last_name="gog",
        password="233sdad34",
        middle_name="ghan gog",
    )

    registered_username = await handler(command)

    assert registered_username == command.username

    user_repo.users[username]

    assert len(event_mediator.published_events) == 1

    assert uow.committed is True
    assert uow.rolled_back is False

    published_event = event_mediator.published_events[0]

    assert published_event.username == command.username
    assert published_event.first_name == command.first_name
    assert published_event.last_name == command.last_name
    assert published_event.middle_name == command.middle_name
