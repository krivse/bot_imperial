from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline_team import team_keyboard
from tgbot.keyboards.inline_tournament import tournament_keyboard
from tgbot.services.db.query import get_about, get_rules
from tgbot.services.set_commands import set_default_commands


async def user_start(message: Message):
    """Приветственное сообщение на команду /start."""
    await message.bot.send_message(
        chat_id=message.from_id,
        text=f'Приветствую, {message.from_user.first_name}, '
             f'в футбольном клубе Империал !')
    await set_default_commands(
        message.bot,
        user_id=message.from_id)


async def about(message: Message, session):
    """Получение описания фк на команду /about."""
    about_info = await get_about(session)

    if about_info is None and message.from_id in message.bot.get('config').tg_bot.admin_ids:
        await message.bot.send_message(
            chat_id=message.from_id,
            text='Информация отсутствует, используйте команду: /change_about'
        )
    elif about_info is None:
        await message.bot.send_message(
            chat_id=message.from_id,
            text='Информация отсутствует!'
        )
    else:
        await message.bot.send_message(
            chat_id=message.from_id,
            text=about_info[0]
        )


async def rules(message: Message, session):
    """Вывод правил фк на команду /rules."""
    rules_info = await get_rules(session)

    if rules_info is None and message.from_id in message.bot.get('config').tg_bot.admin_ids:
        await message.bot.send_message(
            chat_id=message.from_id,
            text='Информация отсутствует, используйте команду: /change_rules'
        )
    elif rules_info is None:
        await message.bot.send_message(
            chat_id=message.from_id,
            text='Информация отсутствует!'
        )
    else:
        await message.bot.send_message(
            chat_id=message.from_id,
            text=rules_info[0]
        )


async def team_list(message: Message, session, state: FSMContext):
    """Команда /team выводит кнопки для вывода информации об игроках."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        text='<b>Показать информацию об игроке</b>',
        reply_markup=await team_keyboard(session)
    )
    await state.update_data(msg_team_list=msg.message_id)


async def player_card(call: CallbackQuery):
    """Отправляется изображение с информацией об игроке."""
    photo = InputFile(f'tgbot/services/pillow/media/player_card/{call.data}.png')
    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo
    )


async def tournament_table(message: Message, session, state: FSMContext):
    """Обработка команды /tournament_table."""
    msg_for_del_tour_t = await message.bot.send_message(
        chat_id=message.from_user.id,
        text='<b>Выберите турнир</b>',
        reply_markup=await tournament_keyboard(session)
    )
    await state.update_data(msg_for_del_tour_t=msg_for_del_tour_t.message_id)


async def user_teams_cancel(call: CallbackQuery, state: FSMContext):
    """Удаляет кнопки и сообщение вызова сведений об игроках."""

    msg = (await state.get_data()).get('msg_team_list')
    if msg is not None:
        await call.message.bot.delete_message(
            chat_id=call.from_user.id,
            message_id=msg
        )
    else:
        await call.message.edit_reply_markup()
    await state.finish()


async def get_tournament_table(call: CallbackQuery, state: FSMContext):
    """Отправляется изображение выбранной турнирной таблицы."""
    name = call.data
    photo = InputFile(f'tgbot/services/pillow/media/tournament_table/{name}_tournament.png')
    await call.message.bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo
    )
    msg_for_del_tour_t = (await state.get_data()).get('msg_for_del_tour_t')
    if msg_for_del_tour_t is not None:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=msg_for_del_tour_t)
    await state.finish()


async def cancel_tournament_table(call: CallbackQuery, state: FSMContext):
    msg_for_del_tour_t = (await state.get_data()).get('msg_for_del_tour_t')

    if msg_for_del_tour_t is not None:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_for_del_tour_t)
    else:
        await call.message.edit_reply_markup()
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart())
    dp.register_message_handler(about, Command('about'))
    dp.register_message_handler(rules, Command('rules'))
    dp.register_message_handler(team_list, Command('team'))
    dp.register_callback_query_handler(user_teams_cancel, text='cancel_keyboard_user')
    dp.register_callback_query_handler(player_card, mode='show_user')
    dp.register_message_handler(tournament_table, Command('tournament_table'))
    dp.register_callback_query_handler(get_tournament_table, mode='tournament_table')
    dp.register_callback_query_handler(cancel_tournament_table, text='cancel_tournament_keyboard')
