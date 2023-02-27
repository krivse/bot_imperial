from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

from tgbot.services.set_commands import set_default_commands


async def admin_start(message: Message):
    """Приветственное сообщение с админом."""
    await message.bot.send_message(message.from_user.id,
        f'<i>Приветствую, </i>{message.from_user.first_name} <i>(admin)</i>\n'
        f'<i>в футбольном клубе Империал!\n'
        f'Изменить правила клуба - /change_about\n'
        f'Изменить описания о клубе - /change_rules\n'
        f'Планировщик событий - /task_scheduler</i>'
    )
    await set_default_commands(
        message.bot,
        user_id=message.from_id
    )


def register_command_start_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, CommandStart(), is_admin=True)
