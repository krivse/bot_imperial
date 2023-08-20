from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.db.query import get_all_users


async def team_keyboard(session, mode=''):
    """Генерация кнопок: "Игроков"."""
    player = await get_all_users(session)

    markup = InlineKeyboardMarkup(row_width=2)
    for name in player:
        first_name, last_name = name[0], name[1]
        markup.insert(InlineKeyboardButton(
            text=f'{first_name} {last_name}',
            callback_data=f'{mode}{first_name}_{last_name}'))
    markup.add(InlineKeyboardButton(
            text='Отмена',
            callback_data=f'{mode}cancel_keyboard_user'))
    return markup
