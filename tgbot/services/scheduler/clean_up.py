def clean_up_old_tasks(scheduler):
    """Очищает старые задания из хранилища после перезапуска."""
    get_jobs = scheduler.get_jobs()
    name = ['team_table', 'tournament_statistics']

    for job in get_jobs:
        if job.name in name:
            job.remove()
