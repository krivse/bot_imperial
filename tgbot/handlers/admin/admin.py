from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import Message, ChatType
from aiogram.dispatcher import Dispatcher

from tgbot.services.set_commands import set_default_commands
from tgbot.handlers.user import about, rules


async def admin_start(message: Message):
    """Приветственное сообщение с админом."""
    await message.bot.send_message(message.from_user.id,
        f'Приветствую, {message.from_user.first_name} (admin)\n'
        f'в футбольном клубе Империал!\n'
        f'Изменить правила клуба - /change_about\n'
        f'Изменить описания о клубе - /change_rules\n'
        f'Планировщик событий - /task_scheduler'
    )
    await set_default_commands(
        message.bot,
        user_id=message.from_id
    )


def register_command_start_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, CommandStart(), is_admin=True)
    dp.register_message_handler(about, Command('about'), is_admin=True)
    dp.register_message_handler(rules, CommandStart('rules'), is_admin=True)
