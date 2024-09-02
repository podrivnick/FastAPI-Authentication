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
    LogoutUserHandler,
)
from src.domain.user.events.authorize_user import AuthorizeUserSchema
from src.domain.user.events.create_user import CreateUserSchema
from src.domain.user.events.logout_user import LogoutUserSchema
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
    mediator.register_command_handler(CreateUserSchema, CreateUserHandler)
    mediator.register_command_handler(AuthorizeUserSchema, AuthorizeUserHandler)
    mediator.register_command_handler(LogoutUserSchema, LogoutUserHandler)
