import pytest
from src.tests.integration.repos.user_create_user_repo import UserRepoMock
from src.tests.mock import EventMediatorMock
from src.tests.mock.uow import UnitOfWorkMock


@pytest.fixture()
def event_mediator() -> EventMediatorMock:
    return EventMediatorMock()


@pytest.fixture()
def uow() -> UnitOfWorkMock:
    return UnitOfWorkMock()


@pytest.fixture()
def user_repo() -> UserRepoMock:
    return UserRepoMock()
