import asyncio
import logging
import tzlocal

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin.description_editor import register_change_description
from tgbot.handlers.admin.schedulers import register_task_admin
from tgbot.handlers.admin.admin import register_command_start_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.middlware_callback import CallbackMiddlware


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, sch):
    cm = CallbackMiddlware()
    dp.setup_middleware(EnvironmentMiddleware(config=config, scheduler=sch))
    dp.setup_middleware(cm)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_command_start_admin(dp)
    register_change_description(dp)
    register_task_admin(dp)
    register_user(dp)


def config_scheduler(bot: Bot, config):
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


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    scheduler = config_scheduler(bot, config)

    bot['config'] = config

    register_all_middlewares(dp, config, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
