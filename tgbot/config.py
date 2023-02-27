from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int

    def construct_sqlalchemy_url(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    group_ids: int
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str

    def dsn(self):
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    redis_config: RedisConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            group_ids=env.int("GROUP"),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            port=env.str('DP_PORT'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(

        ),
        redis_config=RedisConfig(
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            db=env.int('REDIS_DB'),
            password=env.str('REDIS_PASSWORD')
        )
    )
