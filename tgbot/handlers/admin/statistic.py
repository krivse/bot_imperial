from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery, InputFile

from tgbot.handlers.admin.schedulers import tasks_end_date, tasks_start_date
from tgbot.handlers.user import tournament_table
from tgbot.keyboards.inline_statistic import callback_reset_statistics, reset_statistics, statistics, types_name
from tgbot.keyboards.inline_tasks import choice_types
from tgbot.services.db.query import clear_tournament_table_5x5, statistics_publish
from tgbot.services.parsers.team import team_table
from tgbot.services.parsers.tournament import tournament_statistics
from tgbot.services.scheduler.team import team_scheduler


async def form_statistics(message: Message, session, state: FSMContext):
    """Кнопки для выбора действия с событиями."""
    await statistics_publish(session)
    # msg = await message.bot.send_message(
    #     chat_id=message.from_id,
    #     text='<b>Сформировать статистику</b>',
    #     reply_markup=statistics)
    # await state.update_data(
    #     statistics_mode_start=True,
    #     statistics_mode_end=True,
    #     msd_id_collect_statistics=msg.message_id
    # )


async def choice_type_statistics(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Выбрать тип для формирования статистики."""
    types_en = callback_data.get('type_name_en')
    types_ru = callback_data.get('type_name_ru')
    await state.update_data(types_ru=types_en, types_en=types_ru)
    await call.message.bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Вы выбрали статистику: {types_ru}')


async def send_statistics(call: CallbackQuery, state: FSMContext):
    """Отправка статистики."""
    data = await state.get_data()

    photo = InputFile(f'tgbot/services/pillow/media/statistics/.png')
    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo
    )


async def cancel_collect_statistics(call: CallbackQuery, state: FSMContext):
    """Отмена сбора статистики."""
    data = await state.get_data()
    await call.message.edit_reply_markup()
    await call.message.bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=data.get('msd_id_collect_statistics')
    )
    await state.finish()


async def statistics_for_reset(message: Message, state: FSMContext):
    """Команда для сброса статистики."""
    msg = await message.answer('Выберите статистику для сбора', reply_markup=reset_statistics)
    await state.update_data(msg_id_reset_statistics=msg.message_id)


async def select_statistics_for_reset(call: CallbackQuery, session, state: FSMContext):
    """Сброс статистики ЖМФЛЛ 5Х5 ВТД."""
    msg = await state.get_data()

    if call.data == 'reset_statistics_5x5':
        result = await clear_tournament_table_5x5(session)
        await call.answer(result)
    await call.message.edit_reply_markup()
    await call.message.bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=msg.get('msg_id_reset_statistics'),
    )
    await state.finish()


async def cancel_statistics_for_reset(call: CallbackQuery, state: FSMContext):
    """Отмена по сбросу таблицы."""
    msg = await state.get_data()
    await call.message.edit_reply_markup()
    await call.message.bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=msg.get('msg_id_reset_statistics'),
    )
    await state.finish()


async def manual_team_update(message: Message, session):
    """Ручное обновление статистики игроков."""
    msg = await message.answer(
        'Выполняется запрос на обновление статистики по игрокам. После заверения вы получите уведомление. Ожидайте..'
    )
    # tournament_statistics - временно
    await tournament_statistics(session)
    await team_table(session)
    await msg.delete()
    await message.answer('Запрос обработан, можете проверить результат.')


async def manual_tournament_update(message: Message, session):
    """Ручное обновление статистики турнирной таблицы."""
    msg = await message.answer(
        'Выполняется запрос на обновление статистики турнирной таблицы. '
        'После заверения вы получите уведомление. Ожидайте..'
    )
    await tournament_statistics(session)
    await msg.delete()
    await message.answer('Запрос обработан, можете проверить результат.')


def register_statistics_admin(dp: Dispatcher):
    dp.register_message_handler(form_statistics, Command('collect_statistics'), is_admin=True)
    dp.register_callback_query_handler(
        choice_type_statistics, types_name.filter(type_name_en=choice_types), is_admin=True)
    dp.register_callback_query_handler(tasks_start_date, text='start_date', is_admin=True)
    dp.register_callback_query_handler(tasks_end_date, text='end_date', is_admin=True)
    dp.register_callback_query_handler(cancel_collect_statistics, text='cancel_statistics', is_admin=True)
    dp.register_callback_query_handler(send_statistics, text='send', is_admin=True)
    dp.register_message_handler(statistics_for_reset, Command('reset_statistics'), is_admin=True)
    dp.register_callback_query_handler(select_statistics_for_reset, text=callback_reset_statistics, is_admin=True)
    dp.register_callback_query_handler(cancel_statistics_for_reset, text='cancel_reset_statistics', is_admin=True)
    dp.register_message_handler(manual_team_update, Command('update_team'), is_admin=True)
    dp.register_message_handler(manual_tournament_update, Command('update_tournament'), is_admin=True)
