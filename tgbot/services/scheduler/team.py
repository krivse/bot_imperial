from tgbot.services.parsers.team import team_table


def team_scheduler(scheduler: object):
    """Создание задачи для таблицы команды."""

    scheduler.add_job(
        team_table,
        trigger='cron', day_of_week='tue', hour='12'
    )
