import tzlocal

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator

from tgbot.config import Config


def setup_scheduler(bot, config):
    """
    Конфигурация для планировщика событий.
    Незименяемые задачи: 'Туринирная таблица'
                         'Таблица команды'
    """
    job_stores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running"
        )
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(
        timezone=str(tzlocal.get_localzone()), jobstores=job_stores))
    scheduler.ctx.add_instance(bot, declared_class=bot)
    scheduler.ctx.add_instance(config, declared_class=Config)

    return scheduler


def team_scheduler(scheduler):
    'Задача для Туринирная таблица'
    scheduler.add_job(
        # team_statistics,
        trigger='cron', day_of_week='tue', hour='12'
    )
