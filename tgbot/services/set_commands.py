from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat, BotCommandScopeAllGroupChats
from aiogram.bot import Bot


commands = [
    '/start',
    '/team',
    '/about',
    '/rules',
    '/tournament_table',
    'user_manager',
    '/users',
    '/change_about',
    '/change_rules',
    '/task_scheduler',
    '/update_team',
    '/update_tournament'
    # '/collect_statistics',
    # '/reset_statistics',
]


async def set_default_commands(bot: Bot, user_id):
    """
    Команды для пользователя general_commands
    Команды для админа general_commands + дополнительные."""
    general_commands = [
        BotCommand('about', 'О клубе'),
        BotCommand('rules', 'Правила клуба'),
        BotCommand('team', 'Состав команды'),
        # BotCommand('tournament_table', 'Турнирная таблица')
    ]

    if user_id in bot.get('config').tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=[
                *general_commands,
                BotCommand('users', 'Список пользователей'),
                BotCommand('user_manager', 'Менеджер пользователей'),
                BotCommand('change_about', 'Изменить описание клуба'),
                BotCommand('change_rules', 'Изменить правила клуба'),
                BotCommand('update_team', 'Ручное обновление статистики команды'),
                # BotCommand('update_tournament', 'Ручное обновление турнирной таблицы')
                # BotCommand('task_scheduler', 'Планировщик задач')
                # BotCommand('collect_statistics', 'Cтатистика опросов'),
                # BotCommand('reset_statistics', 'Сброс статистики')

            ],
            scope=BotCommandScopeAllPrivateChats(user_id)
        )
    else:
        await bot.set_my_commands(
            commands=general_commands,
            scope=BotCommandScopeAllGroupChats()
        )
