from dataclasses import dataclass

from src.settings.config import (
    API_HOST,
    API_PORT,
)


@dataclass
class APIConfig:
    host: str = API_HOST
    port: int = API_PORT
    reload: bool = True
    debug: bool = __debug__
