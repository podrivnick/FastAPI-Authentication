import punq
from didiator import (
    CommandMediator,
    EventMediator,
    Mediator,
    QueryMediator,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.user import UserRepo
from src.infrastructure.db.main import (
    build_sa_engine,
    build_sa_session,
    build_sa_session_factory,
)
from src.infrastructure.db.repositories.users import UserRepoAlchemyImpl
from src.infrastructure.mediator import get_mediator
from src.infrastructure.uow import build_uow


def setup_container() -> punq.Container:
    container = punq.Container()

    container.register(UnitOfWork, factory=build_uow, scope=punq.Scope.REQUEST)
    setup_mediator_factory(container)
    setup_db_factories(container)

    return container


def setup_mediator_factory(container: punq.Container) -> None:
    container.register(Mediator, factory=get_mediator, scope=punq.Scope.REQUEST)
    container.register(QueryMediator, factory=get_mediator, scope=punq.Scope.REQUEST)
    container.register(CommandMediator, factory=get_mediator, scope=punq.Scope.REQUEST)
    container.register(EventMediator, factory=get_mediator, scope=punq.Scope.REQUEST)


def setup_db_factories(container: punq.Container) -> None:
    container.register(AsyncEngine, factory=build_sa_engine, scope=punq.Scope.SINGLETON)
    container.register(
        async_sessionmaker[AsyncSession],
        factory=build_sa_session_factory,
        scope=punq.Scope.SINGLETON,
    )
    container.register(AsyncSession, factory=build_sa_session, scope=punq.Scope.REQUEST)
    container.register(UserRepo, factory=UserRepoAlchemyImpl, scope=punq.Scope.REQUEST)
