from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat
from aiogram.bot import Bot


async def set_default_commands(bot: Bot, user_id):
    general_commands = [
        BotCommand('about', 'О клубе'),
        BotCommand('rules', 'Правила клуба'),
        BotCommand('team', 'Состав команды'),
        BotCommand('statistic', 'Cтатистика матчей')
    ]

    if user_id in bot.get('config').tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=[
                *general_commands,
                BotCommand('change_about', 'Изменить описание о клубе'),
                BotCommand('change_rules', 'Изменить описание правил клуба'),
                BotCommand('task_scheduler', 'Планировщик задач')
            ],
            scope=BotCommandScopeChat(user_id)
        )
    else:
        await bot.set_my_commands(
            commands=general_commands,
            scope=BotCommandScopeAllPrivateChats()
        )
