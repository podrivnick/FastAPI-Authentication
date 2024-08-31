from dataclasses import (
    dataclass,
    field,
)

from di import bind_by_type
from di.dependent import Dependent
from didiator.interface.utils.di_builder import DiBuilder
from src.infrastructure.db.config import (
    DBConfig,
    RedisConfig,
)
from src.infrastructure.di import DiScope
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


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    api: APIConfig = field(default_factory=APIConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config),
    )
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DBConfig),
    )
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: config.api, scope=DiScope.APP), APIConfig),
    )
    di_builder.bind(
        bind_by_type(
            Dependent(lambda *args: config.redis, scope=DiScope.APP),
            RedisConfig,
        ),
    )
