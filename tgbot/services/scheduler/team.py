from tgbot.services.parsers.team import team_table


def team_scheduler(scheduler: object, instance_sess):
    """Создание задачи для таблицы команды."""
    setattr(team_table, 'session', instance_sess)

    scheduler.add_job(
        team_table,
        trigger='cron', day_of_week='tue', hour='12'
    )
