from sqlalchemy import select

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.db.models import Team


async def team_keyboard(session):
    """Генерация кнопок: "Игроков"."""
    player = await select_players(session)
    markup = InlineKeyboardMarkup(row_width=2)
    for name in player:
        first_name, last_name = name[0].split()[0], name[0].split()[1]
        markup.insert(InlineKeyboardButton(
            text=f'{first_name} {last_name}',
            callback_data=f'{first_name}_{last_name}'))
    markup.add(InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'))
    return markup


async def select_players(session):
    """Выборка имен игроков."""
    player = select(
        Team.gamer,
    )
    return (await session.execute(player)).all()
