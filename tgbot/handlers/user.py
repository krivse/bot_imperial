from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import CommandStart


from tgbot.keyboards.inline_team import team_keyboard
from tgbot.services.set_commands import set_default_commands


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


async def team_list(message: Message, session):
    """Команда /team выводит кнопки для вывода информации об игроках."""
    await message.bot.send_message(
        chat_id=message.from_id,
        text='Показать информацию об игроке:',
        reply_markup=await team_keyboard(session)
    )


async def player_card(callback: CallbackQuery):
    """Отправляется изображение с информацией об игроке."""
    photo = InputFile(f'tgbot/services/pillow/media/player_card/{callback.data}.png')
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo
    )


async def statistic_list(message: Message):
    """Отправляется изображение с текущей статистикой по турниру 5х5."""
    photo = InputFile('tgbot/services/pillow/media/statistic/tournament.png')
    await message.bot.send_photo(
        chat_id=message.from_id,
        photo=photo
    )


async def user_teams_cancel(callback: CallbackQuery):
    """Удаляет кнопки и сообщение вызова сведений об игроках."""
    await callback.message.delete()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart())
    dp.register_message_handler(about, Command('about'))
    dp.register_message_handler(rules, Command('rules'))
    dp.register_message_handler(team_list, Command('team'))
    dp.register_callback_query_handler(user_teams_cancel, text='cancel')
    dp.register_callback_query_handler(player_card)
    dp.register_message_handler(statistic_list, Command('statistic'))
