from aiogram.dispatcher import Dispatcher


async def add_jobs_in_scheduler(data, scheduler):
    """Создание события в scheduler с помощью cron."""
    start_date = data['start_date']
    end_date = data['end_date']
    types_en = data['type_en']
    day_en = data['day_en']
    scheduler.add_job(
        voting_scheduler,
        trigger='cron', start_date=start_date, end_date=end_date, day_of_week=day_en, hour='12',
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
        trigger='cron', start_date=start_date, end_date=end_date, day_of_week=day_en, hour='14')


async def voting_scheduler(data: dict):
    """Вывод голосования при наступлении события."""
    dp = Dispatcher.get_current()
    title = data['title']
    await dp.bot.send_poll(
        chat_id=-1001826545007,
        question=title,
        options=['Буду', 'Не смогу'],
        is_anonymous=False,
        disable_notification=True)
