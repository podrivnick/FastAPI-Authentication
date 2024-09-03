import pytest
from src.application.user.commands.authentication import AuthorizeUserHandler
from src.domain.user.events import AuthorizeUserSchema
from src.tests.integration.repos.user_login_repo import UserAuthenticationRepoMock
from src.tests.mock.event_mediator import EventMediatorMock


@pytest.mark.asyncio
async def test_login_handler(
    user_auth_repo: UserAuthenticationRepoMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = AuthorizeUserHandler(user_auth_repo, event_mediator)

    command = AuthorizeUserSchema(
        username="koshka",
        password="Password1",
    )

    authentication_token = await handler(command)

    assert authentication_token is not None

    assert len(event_mediator.published_events) == 1

    published_event = event_mediator.published_events[0]

    assert published_event.username == command.username
    assert published_event.username == command.username
