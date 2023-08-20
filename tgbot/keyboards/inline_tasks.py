from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


tasks = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать', callback_data='create'),
        ],
        [
            InlineKeyboardButton(text='Изменить', callback_data='edit')
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data='delete')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

types_callback = CallbackData('types', 'type_name_ru', 'type_name_en', 'accusative')
choice_types = ['game', 'training', 'training_2', 'best_player']
choice_types_tasks = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Игра', callback_data=types_callback.new(
                type_name_ru='Игра', type_name_en='game', accusative='игру'
            ))
        ],
        [
            InlineKeyboardButton(text='Тренировка', callback_data=types_callback.new(
                type_name_ru='Тренировка', type_name_en='training', accusative='тренировку'
            ))
        ],
        [
            InlineKeyboardButton(text='Тренировка 2', callback_data=types_callback.new(
                type_name_ru='Тренировка 2', type_name_en='training_2', accusative='тренировку 2'
            ))
        ],
        # [
        #     InlineKeyboardButton(text='Лучший игрок', callback_data=types_callback.new(
        #         type_name_ru='Лучший игрок', type_name_en='best_player', accusative='Лучшего и-ка'
        #     ))
        # ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back_tasks'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)


input_data_tasks = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Название', callback_data='title'),
            InlineKeyboardButton(text='День', callback_data='day'),
        ],
        [
            InlineKeyboardButton(text='Дата начала', callback_data='start_date'),
            InlineKeyboardButton(text='Дата окончания', callback_data='end_date')
        ],
        [
            InlineKeyboardButton(text='Продолжить', callback_data='continue')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back_types'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

days_callback = CallbackData('days', 'day_ru', 'day_en')
days_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
choice_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ПН', callback_data=days_callback.new(day_ru='Понедельник', day_en='mon')),
            InlineKeyboardButton(text='ВТ', callback_data=days_callback.new(day_ru='Вторник', day_en='tue')),
            InlineKeyboardButton(text='СР', callback_data=days_callback.new(day_ru='Среда', day_en='wed')),
            InlineKeyboardButton(text='ЧТ', callback_data=days_callback.new(day_ru='Четверг', day_en='thu')),
            InlineKeyboardButton(text='ПТ', callback_data=days_callback.new(day_ru='Пятница', day_en='fri')),
            InlineKeyboardButton(text='СБ', callback_data=days_callback.new(day_ru='Суббота', day_en='sat')),
            InlineKeyboardButton(text='ВС', callback_data=days_callback.new(day_ru='Воскресенье', day_en='sun'))
        ]
    ]
)
