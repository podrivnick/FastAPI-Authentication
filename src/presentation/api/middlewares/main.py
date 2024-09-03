from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .configure_state import set_request_id_middleware
from .structlog import structlog_bind_middleware


def setup_middleware(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=structlog_bind_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
