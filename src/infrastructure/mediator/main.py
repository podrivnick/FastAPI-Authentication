import logging

from didiator import (
    CommandDispatcherImpl,
    EventObserverImpl,
    Mediator,
    MediatorImpl,
    QueryDispatcherImpl,
)
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import (
    DiMiddleware,
    DiScopes,
)
from didiator.middlewares.logging import LoggingMiddleware
from src.application.user.commands import (
    AuthorizeUserHandler,
    CreateUserHandler,
)
from src.domain.user.events.authorize_user import AuthorizeUser
from src.domain.user.events.create_user import CreateUser
from src.infrastructure import di


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(di.DiScope.REQUEST)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(CreateUser, CreateUserHandler)
    mediator.register_command_handler(AuthorizeUser, AuthorizeUserHandler)
