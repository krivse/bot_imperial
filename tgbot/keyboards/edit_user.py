from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_type_user_work_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='add_user')
        ],
        [
            InlineKeyboardButton(text='Редактировать', callback_data='edit_user')
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data='delete_user')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_start_menu_manager_user')
        ]
    ]
)

credentials = [
    'first_name', 'last_name', 'middle_name', 'birthday', 'phone', 'avatar', 'current_club', 'role', 'telegram_id'
]
mode_edit_user_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Имя', callback_data='first_name'),
            InlineKeyboardButton(text='Фамилия', callback_data='last_name')
        ],
        [
            InlineKeyboardButton(text='Отчество', callback_data='middle_name'),
            InlineKeyboardButton(text='Дата рождения', callback_data='birthday')
        ],
        [
            InlineKeyboardButton(text='Фото профиля', callback_data='avatar'),
            InlineKeyboardButton(text='Позиция', callback_data='role'),
            InlineKeyboardButton(text='Клуб', callback_data='current_club')
        ],
        # [
        #     InlineKeyboardButton(text='Позиция', callback_data='role')
        # ],
        [
            InlineKeyboardButton(text='Телефон', callback_data='phone'),
            InlineKeyboardButton(text='Телеграм id', callback_data='telegram_id'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_menu_manager_user')
        ]
    ]
)

create_user_db = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='create_user'),
            InlineKeyboardButton(text='Отменить', callback_data='cancel_create_user')
        ]
    ]
)

cancel_editor_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить', callback_data='cancel_editor_user')
        ]
    ]
)
