from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

types_name = CallbackData('types', 'type_name_ru', 'type_name_en')
statistics = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Дата начала', callback_data='start_date'),
            InlineKeyboardButton(text='Дата окончания', callback_data='end_date')
        ],
        [
            InlineKeyboardButton(text='Игра', callback_data=types_name.new(
                type_name_ru='Игра', type_name_en='game'
            ))
        ],
        [
            InlineKeyboardButton(text='Тренировка', callback_data=types_name.new(
                type_name_ru='Тренировка', type_name_en='training'
            ))
        ],
        [
            InlineKeyboardButton(text='Тренировка 2', callback_data=types_name.new(
                type_name_ru='Тренировка 2', type_name_en='training_2'
            ))
        ],
        [
            InlineKeyboardButton(text='Лучший игрок', callback_data=types_name.new(
                type_name_ru='Лучший игрок', type_name_en='best_player'
            ))
        ],
        [
            InlineKeyboardButton(text='Отправить', callback_data='send'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_statistics')
        ]
    ]
)


callback_reset_statistics = ['reset_statistics_5x5']
reset_statistics = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ЖМФЛЛ 5Х5 ВТД', callback_data='reset_statistics_5x5'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_reset_statistics')
        ]
    ]
)
