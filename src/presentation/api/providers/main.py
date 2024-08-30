from didiator import (
    CommandMediator,
    EventMediator,
    Mediator,
    QueryMediator,
)
from fastapi import FastAPI
from punq import Container

from .mediator import MediatorProvider


def setup_providers(app: FastAPI, container: Container) -> None:
    mediator = container.resolve(Mediator)
    mediator_provider = MediatorProvider(mediator)

    app.dependency_overrides[CommandMediator] = mediator_provider.build
    app.dependency_overrides[QueryMediator] = mediator_provider.build
    app.dependency_overrides[EventMediator] = mediator_provider.build
    app.dependency_overrides[Mediator] = mediator_provider.build

    app.dependency_overrides[Container] = lambda: container
