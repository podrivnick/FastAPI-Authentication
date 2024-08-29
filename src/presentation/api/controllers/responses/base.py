from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)


TResult = TypeVar("TResult")
TException = TypeVar("TException")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class SuccessResponse(Response, Generic[TResult]):
    status: int = 200
    result: TException | None = field(default=None)


@dataclass(frozen=True)
class ErrorData(Generic[TException]):
    title: str = "Unknown error occurred"
    data: TException | None = None


@dataclass(frozen=True)
class FailureResponse(Response, Generic[TException]):
    status: int = 500
    error: ErrorData[TException] = field(default_factory=ErrorData)
