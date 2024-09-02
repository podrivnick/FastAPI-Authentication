import pytest
from src.application.user.commands.logout import LogoutUserHandler
from src.domain.user.events.logout_user import LogoutUserSchema
from src.tests.integration.repos.user_logout_repo import UserLogoutedRepoMock
from src.tests.mock.event_mediator import EventMediatorMock


@pytest.mark.asyncio
async def test_logout_handler(
    user_logout_repo: UserLogoutedRepoMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = LogoutUserHandler(user_logout_repo, event_mediator)

    command = LogoutUserSchema(
        token="sfdsdfsdfs6df6sd6f53e6edf63ws6efesf",
    )
    await handler(command)

    # with pytest.raises(exceptions_domain.TokenAuthorisationNotFoundException) as exc_info:  noqa
    #     logout = await handler(command)  noqa

    # assert exc_info.value.message == "Token not found in the database."   noqa

    assert len(event_mediator.published_events) == 1

    published_event = event_mediator.published_events[0]

    assert published_event.auth_token == command.token