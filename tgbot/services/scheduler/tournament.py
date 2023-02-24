from tgbot.services.parsing_record.tournament import tournament_statistics


def tournament_scheduler(scheduler: object, instance_sess):
    """Создание задачи для турнирной таблицы."""
    setattr(tournament_statistics, 'session', instance_sess)
    scheduler.add_job(
        tournament_statistics,
        # trigger='cron', day_of_week='wed', hour='12'
    )