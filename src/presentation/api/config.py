from dataclasses import dataclass

from config import (
    API_HOST,
    API_PORT,
)


@dataclass
class APIConfig:
    host: str = API_HOST
    port: int = API_PORT
    reload: bool = True
    debug: bool = __debug__
