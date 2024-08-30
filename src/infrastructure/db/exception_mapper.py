from collections.abc import (
    Callable,
    Coroutine,
)
from functools import wraps
from typing import (
    Any,
    ParamSpec,
    TypeVar,
)

from sqlalchemy.exc import SQLAlchemyError
from src.application.common import exceptions


Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
Func = Callable[Param, ReturnType]


def exception_mapper(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise exceptions.RepoException from err

    return wrapped
