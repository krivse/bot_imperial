from tgbot.services.parsers.tournament import tournament_statistics


def tournament_scheduler(scheduler: object):
    """Создание задачи для турнирной таблицы."""

    scheduler.add_job(
        tournament_statistics,
        trigger='cron', day_of_week='tue', hour='12'
    )
