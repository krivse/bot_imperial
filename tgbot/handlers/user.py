from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import CommandStart


from tgbot.keyboards.inline_team import team
from tgbot.services.set_commands import set_default_commands
# from tgbot.services.db.querys import show_ttable


async def user_start(message: Message):
    await message.bot.send_message(
        chat_id=message.from_id,
        text=f'Приветствую, {message.from_user.first_name}\n'
             f'в футбольном клубе Империал !')
    await set_default_commands(
        message.bot,
        user_id=message.from_id)


async def about(message: Message):
    await message.bot.send_message(chat_id=message.from_id, text='Здесь будет размещена информация о клубе !')


async def rules(message: Message):
    await message.bot.send_message(
        chat_id=message.from_id,
        text='Здесь будет описаны правила в клубе !'
    )


async def team_list(message: Message):
    await message.bot.send_message(
        chat_id=message.from_id,
        text='Информация о члене команды отправляется в приватный чат!',
        reply_markup=team
    )


async def user_teams(callback: CallbackQuery):
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Информация об игроке: {callback.data}'
    )


async def statistic_list(message: Message, session):
    await message.bot.send_message(
        chat_id=message.from_id,
        text='Стастика команды в турнирной таблице отправляется в приватный чат!'
    )


async def user_teams_cancel(callback: CallbackQuery):
    await callback.message.edit_reply_markup()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart())
    dp.register_message_handler(about, Command('about'))
    dp.register_message_handler(rules, Command('rules'))
    dp.register_message_handler(team_list, Command('team'))
    dp.register_message_handler(statistic_list, Command('statistic'))
    dp.register_callback_query_handler(user_teams_cancel, text='cancel')
