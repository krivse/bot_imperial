from aiogram.dispatcher import Dispatcher

from tgbot.services.db.query import create_poll

from aiogram import Bot
from sqlalchemy.orm import sessionmaker


async def add_jobs_in_scheduler(data, session, scheduler):
    """Создание события в scheduler с помощью cron."""
    start_date = data['start_date']
    end_date = data['end_date']
    types_en = data['type_en']
    day_en = data['day_en']
    bot = Dispatcher.get_current().bot
    instance = {'dp': bot, 'session': session}
    setattr(voting_scheduler, 'instance', instance)
    scheduler.add_job(
        voting_scheduler,
        trigger='cron', start_date=start_date, end_date=end_date, day_of_week=day_en, hour='0-23', minute='*/1',
        kwargs={'data': data},
        name=types_en,
    )


async def modify_jobs_in_scheduler(data, scheduler):
    """Изменение события в scheduler."""
    job_id = data.get('job_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    types_en = data.get('type_en')
    day_en = data.get('day_en')
    scheduler.modify_job(
        job_id=job_id,
        func=voting_scheduler,
        kwargs={'data': data},
        name=types_en
    )
    scheduler.reschedule_job(
        job_id=job_id,
        trigger='cron', start_date=start_date, end_date=end_date, day_of_week=day_en, hour='12')


async def voting_scheduler(bot: Bot, session_pool: sessionmaker, data: dict):
    """Вывод голосования при наступлении события."""
    title = data['title']
    type_ru = data['type_ru']
    # if 'type_ru' != 'type_ru':
    #     options = await best_player(session)
    #     print(options)
    # else:
    options = ['Буду', 'Не смогу']
    message = await bot.send_poll(
        chat_id=bot.get('config').tg_bot.group_ids,
        question=title,
        options=options,
        is_anonymous=False,
        disable_notification=True,
    )
    await create_poll(session_pool, type_ru, message.poll.id)
    await bot.pin_chat_message(chat_id=bot.get('config').tg_bot.group_ids, message_id=message.message_id)


# async def best_player(session):
#     options = []
#     player = await select_players(session)
#     for name in player:
#         first_name, last_name = name[0].split()[0], name[0].split()[1]
#         options.append(f'{first_name} {last_name}')
#     return options
