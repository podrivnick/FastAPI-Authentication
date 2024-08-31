from asyncio_redis import Connection
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession, connection_redis: Connection) -> None:
        self._session = session
        self._connection_redis = connection_redis
