from dataclasses import dataclass

from config import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USER,
)


@dataclass
class DBConfig:
    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://%{DATABASE_USER}s:%{DATABASE_PASSWORD}s@%{DATABASE_HOST}s:%{DATABASE_PORT}s/%{DATABASE_NAME}s?async_fallback=True"
