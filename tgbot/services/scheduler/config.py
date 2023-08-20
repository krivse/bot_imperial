import tzlocal

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator

from aiogram import Bot

from sqlalchemy.orm import sessionmaker

from tgbot.config import Config, load_config


def setup_scheduler(bot, config, session_pool):
    """
    Конфигурация для планировщика событий.
    Незименяемые задачи: 'Туринирная таблица'
                         'Таблица команды'.
    """
    if not config:
        config = load_config()
    job_stores = {
        "default": RedisJobStore(
            # db=config.redis_config.db,
            # host=config.redis_config.host,
            # password=config.redis_config.password,
            # port=config.redis_config.port,
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running"
        )
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(
        timezone=str(tzlocal.get_localzone()), jobstores=job_stores))

    if not bot:
        bot = Bot(config.tg_bot.token)
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.ctx.add_instance(config, declared_class=Config)
    scheduler.ctx.add_instance(session_pool, declared_class=sessionmaker)

    return scheduler
