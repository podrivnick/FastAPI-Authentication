import pytest
from src.tests.integration.repos.user_create_user_repo import UserRepoMock
from src.tests.integration.repos.user_login_repo import UserAuthenticationRepoMock
from src.tests.integration.repos.user_logout_repo import UserLogoutedRepoMock
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


@pytest.fixture()
def user_auth_repo() -> UserAuthenticationRepoMock:
    return UserAuthenticationRepoMock()


@pytest.fixture()
def user_logout_repo() -> UserLogoutedRepoMock:
    return UserLogoutedRepoMock()
