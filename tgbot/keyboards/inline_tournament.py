from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.db.query import get_all_tournament_table, get_all_users


async def tournament_keyboard(session):
    """Генерация списка турнирных таблицы."""
    tournament_table = await get_all_tournament_table(session)

    markup = InlineKeyboardMarkup(row_width=2)
    for name in tournament_table:
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=name.replace(' ', '_')
        ))
    markup.add(InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_tournament_keyboard'))
    return markup
