import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from presentation.api.controllers import setup_controllers

from .config import APIConfig


async def init_api(
    debug: bool = __debug__,
) -> FastAPI:
    app = FastAPI(
        debug=debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )

    setup_controllers(app)

    return app


async def run_api(
    app: FastAPI,
    api_config: APIConfig,
) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
    )
    server = uvicorn.Server(config)

    await server.serve()
