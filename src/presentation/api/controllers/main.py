from fastapi import FastAPI

from .default import default_router
from .user import user_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(user_router)
