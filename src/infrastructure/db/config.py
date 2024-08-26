from dataclasses import dataclass


@dataclass
class DBConfig:
    DATABASE_HOST: str = "postgres"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "auth_fastapi"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "1234"

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://%{self.DATABASE_USER}s:%{self.DATABASE_PASSWORD}s@%{self.DATABASE_HOST}s:%{self.DATABASE_PORT}s/%{self.DATABASE_NAME}s?async_fallback=True"
