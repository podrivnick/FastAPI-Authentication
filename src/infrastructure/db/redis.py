import asyncio_redis

from .config import RedisConfig


async def init_connection_redis(
    redis_config: RedisConfig,
) -> asyncio_redis.Connection:
    connection_redis = await asyncio_redis.Connection.create(
        host=redis_config.host,
        port=redis_config.port,
    )

    yield connection_redis
