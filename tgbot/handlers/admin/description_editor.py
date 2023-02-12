from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message


async def change_about(message: Message):
    await message.bot.send_message(chat_id=message.from_id, text='change_about')


async def change_rules(message: Message):
    await message.bot.send_message(chat_id=message.from_id, text='change_rules')


def register_change_description(dp: Dispatcher):
    dp.register_message_handler(change_about, Command('change_about'), is_admin=True)
    dp.register_message_handler(change_rules, Command('change_rules'), is_admin=True)
