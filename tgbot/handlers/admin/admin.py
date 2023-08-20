from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

from tgbot.services.set_commands import set_default_commands


async def admin_start(message: Message):
    """Приветственное сообщение с админом."""
    await message.bot.send_message(
        message.from_user.id,
        f'Приветствую, {message.from_user.first_name} <i>(admin)</i>\n'
        'в футбольном клубе Империал!\n'
        'Описание клуба - /about\n'
        'Правила клуба - /rules\n'
        'Состав команды - /team\n'
        'Список пользователей - /users\n'
        'Турнирная таблица - /tournament_table\n'
        'Изменить описание клуба - /change_about\n'
        'Изменить правила клуба - /change_rules\n'
        'Планировщик событий - /task_scheduler\n'
        'Редактор пользователей - /user_manager'
    )
    await set_default_commands(
        message.bot,
        user_id=message.from_id
    )


def register_command_start_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, CommandStart(), is_admin=True)
