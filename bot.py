#!/usr/bin/python3
import asyncio
import logging

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter, UserFilter
from tgbot.handlers.admin.description_editor import register_change_description_admin
from tgbot.handlers.admin.schedulers import register_task_admin
from tgbot.handlers.admin.admin import register_command_start_admin
from tgbot.handlers.admin.statistic import register_statistics_admin
from tgbot.handlers.admin.user_editor import register_users_admin
from tgbot.handlers.errors import register_errors_handler
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.stop_flood import CheckFlood
from tgbot.services.db.config import create_session_pool
from tgbot.services.scheduler.clean_up import clean_up_old_tasks
from tgbot.services.scheduler.config import setup_scheduler
from tgbot.services.scheduler.tournament import tournament_scheduler
from tgbot.services.scheduler.team import team_scheduler


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, scheduler, session_pool):
    dp.setup_middleware(EnvironmentMiddleware(config=config, scheduler=scheduler))
    dp.setup_middleware(DatabaseMiddleware(session_pool=session_pool))
    dp.setup_middleware(CheckFlood())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(UserFilter)


def register_all_handlers(dp):
    register_users_admin(dp)
    register_statistics_admin(dp)
    register_command_start_admin(dp)
    register_change_description_admin(dp)
    register_task_admin(dp)
    register_user(dp)
    register_errors_handler(dp)


def plan_jobs(scheduler, session):
    clean_up_old_tasks(scheduler)
    tournament_scheduler(scheduler, session)
    team_scheduler(scheduler, session)


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

    bot['config'] = config

    session_pool = await create_session_pool(db=config.db, echo=False)
    scheduler = setup_scheduler(bot, config, session_pool)

    register_all_middlewares(dp, config, scheduler, session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
        plan_jobs(scheduler, session_pool)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
