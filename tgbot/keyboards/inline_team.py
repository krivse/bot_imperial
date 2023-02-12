from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


team = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Виктор Васильев', callback_data='Виктор Васильев'),
            InlineKeyboardButton(text='Иван Красников', callback_data='Иван Красников')
        ],
        [
            InlineKeyboardButton(text='Павел Барков', callback_data='Павел Барков')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)
