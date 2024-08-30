import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from src.presentation.api.controllers import setup_controllers

from .config import APIConfig


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://0.0.0.0:8000",
    "*",
]


async def init_api(
    debug: bool = __debug__,
) -> FastAPI:
    app = FastAPI(
        debug=debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    setup_providers(app, mediator, di_builder, di_state)
    setup_controllers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )

    return app


async def run_api(
    app: FastAPI,
    api_config: APIConfig,
) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        reload=True,
    )
    server = uvicorn.Server(config)

    await server.serve()
