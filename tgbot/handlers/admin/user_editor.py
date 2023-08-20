import re

from aiogram.types import CallbackQuery, Message, InputFile
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.keyboards.edit_user import cancel_editor_user, create_user_db, credentials, mode_edit_user_keyboard, \
    select_type_user_work_keyboard
from tgbot.keyboards.inline_team import team_keyboard
from tgbot.misc.states import UserState
from tgbot.services.db.query import add_user, delete_user, edit_user, get_all_users, get_phone, get_telegram_id
from tgbot.services.pillow.team_img import show_table_player
from tgbot.services.set_commands import commands


async def users_admin(message: Message, state: FSMContext):
    """
    Механизм по работе с пользователями
    Вывод кнопок для Создания / Редактирования / Удаления.
    """
    cancel_menu_manager_user = await message.bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите нужный пункт меню',
        reply_markup=select_type_user_work_keyboard)
    await state.update_data(cancel_menu_manager_user=cancel_menu_manager_user.message_id)


async def add_user_admin(call: CallbackQuery, state: FSMContext):
    """
    Добавление пользователя с помощью FSMState,
    который реализует 8 уровней сбора данных.
    """
    state_data = await state.get_data()

    cancel_menu_manager_user = state_data.get('cancel_menu_manager_user')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=cancel_menu_manager_user)

    msg_cancel_editor_user = await call.message.answer(
        'Перешлите сообщение от пользователя или введите его telegram_id, '
        'которого необходимо добавить', reply_markup=cancel_editor_user)
    await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
    await UserState.telegram_id.set()


async def telegram_id_user(message: Message, session, state: FSMContext):
    """Получение от админа telegram_id пользователя."""
    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    msg = message.forward_from.id if message.forward_from is not None else message.text
    telegram_id = int(msg) if msg.isdigit() else False

    if telegram_id:
        exists_user = await get_telegram_id(session, int(telegram_id))
    else:
        msg_cancel_editor_user = await message.answer(
            'ID пользователя может состоять только из цифр! Попробуйте ещё раз.'
            'Необходимо переслать сообщение конкретного пользователя, которого собираетесь добавить!'
            'Я помогу :-) Лучше всего выберите любое сообщение от пользователя, зажмите его '
            'и в выпадающем меню выбери пункт "переслать".',
            reply_markup=cancel_editor_user
        )
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
        return False

    if exists_user is not None and state_data.get('edit_telegram_id') is None:
        msg_cancel_editor_user = await message.answer(
            f'Пользователь с таким telegram_id уже существует под именем: {exists_user[1]} {exists_user[2]}. '
            'Введите новый или нажмите на кнопку отмены!',
            reply_markup=cancel_editor_user
        )
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)

    elif telegram_id and state_data.get('edit_telegram_id') is True:
        # режим редактирования telegram_id
        db_first_name = state_data.get('calldata_first_name')
        db_last_name = state_data.get('calldata_last_name')
        result = await edit_user(session, db_first_name, db_last_name, e_telegram_id=telegram_id)
        await show_table_player(session, user=result.id)
        await message.answer(f'{db_first_name} {db_last_name} '
                             f'присвоен телеграм-аккаунт: {result.telegram_id}')
        await state.reset_state(with_data=False)
    else:
        await state.update_data(telegram_id=int(telegram_id))
        await UserState.full_name.set()
        msg_cancel_editor_user = await message.answer(
            'Введите ФИО в формате: Иванов Иван Иванович',
            reply_markup=cancel_editor_user
        )
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def full_name_user(message: Message, state: FSMContext):
    """Получение full_name пользователя."""
    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    msg = message.text.split(' ')

    if len(msg) < 2:
        msg_cancel_editor_user = await message.answer(
            'Необходимо передать хотя бы фамилию и имя!',
            reply_markup=cancel_editor_user
        )
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
    else:
        fio = []
        for el in msg:
            if el != '':
                fio.append(el.capitalize())

        first_name, last_name, middle_name = fio[0], fio[1], '-'

        if len(fio) > 2:
            middle_name = fio[2]
        if not any([first_name.isdigit(), last_name.isdigit(), middle_name.isdigit()]):
            msg_cancel_editor_user = await message.answer(
                'Введите дату рождения в формате: ДД/ММ/ГГГГ',
                reply_markup=cancel_editor_user
            )
            await state.update_data(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                msg_cancel_editor_user=msg_cancel_editor_user.message_id
            )
            await UserState.birthday.set()
        else:
            msg_cancel_editor_user = await message.answer(
                'ФИО не может быть из цифр!',
                reply_markup=cancel_editor_user
            )
            await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def birthday_user(message: Message, session, state: FSMContext):
    """Получение birthday пользователя."""
    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    birthday = message.text
    frt_bd = re.sub(r'[. -]', '/', birthday)
    day, month, year = frt_bd[:2], frt_bd[3:5], frt_bd[-4:]

    if all([day.isdigit(), month.isdigit(), year.isdigit()]):
        if all([1 <= int(day) <= 31, 1 <= int(month) <= 12, 1950 <= int(year) <= 2100]):
            # режим редактирования даты рождения пользователя
            if state_data.get('edit_birthday'):
                db_first_name = state_data.get('calldata_first_name')
                db_last_name = state_data.get('calldata_last_name')
                result = await edit_user(session, db_first_name, db_last_name, e_birthday=frt_bd)
                await show_table_player(session, user=result.id)
                await message.answer(f'{db_first_name} {db_last_name} новая дата рождения: {result.birthday} ')
                await state.update_data(edit_birthday=False)
                await state.reset_state(with_data=False)
            else:
                # режим добавления пользователя
                await state.update_data(birthday=frt_bd)
                await UserState.phone.set()
                msg_cancel_editor_user = await message.answer(
                    'Введите номер телефона',
                    reply_markup=cancel_editor_user
                )
                await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
        else:
            msg_cancel_editor_user = await message.answer(
                'Введите корректную дату, в формате ДД/ММ/ГГГГ\n'
                f'Вы ввели {birthday}.',
                reply_markup=cancel_editor_user
            )
            await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
    else:
        msg_cancel_editor_user = await message.answer(
            'Введите корректную дату, в формате ДД/ММ/ГГГГ\n'
            f'Вы ввели {birthday}.',
            reply_markup=cancel_editor_user
        )
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def phone_user(message: Message, session, state: FSMContext):

    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    phone = message.text
    format_phone = re.sub(r'[+() -]', '', phone).replace(phone[0], '7', 1)

    if format_phone.isdigit() and len(format_phone) == 11:

        exists_user = await get_phone(session, int(format_phone))
        if exists_user is not None and state_data.get('edit_telegram_id') is None:
            msg_cancel_editor_user = await message.answer(
                f'Пользователь с таким номером телефона уже существует под именем: {exists_user[1]} {exists_user[2]}',
                reply_markup=cancel_editor_user)
            await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
            return False

        # режим редактирования даты рождения пользователя
        if state_data.get('edit_phone'):
            db_first_name = state_data.get('calldata_first_name')
            db_last_name = state_data.get('calldata_last_name')
            result = await edit_user(session, db_first_name, db_last_name, e_phone=format_phone)
            await message.answer(f'{db_first_name} {db_last_name} новый номер телефона: {result.phone} ')
            await state.update_data(edit_phone=False)
            await state.reset_state(with_data=False)
        else:
            # режим добавления пользователя
            await state.update_data(phone=format_phone)
            await UserState.role.set()
            msg_cancel_editor_user = await message.answer(
                'Введите амплуа игрока, например: НАП или Нападающий',
                reply_markup=cancel_editor_user
            )
            await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)
    else:
        msg_cancel_editor_user = await message.answer(
            f'Вы ввели - {phone}!\n'
            'Проверьте, что номер был введен корректно и попробуйте снова.\n'
            'Попробуйте ввести в формате 79997775533',
            reply_markup=cancel_editor_user)
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def role_user(message: Message, session, state: FSMContext):
    """Получение role пользователя."""
    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    if message.text not in commands and not message.text.isdigit():
        role = message.text.lower()
        if role == 'защитник':
            role = 'ЗАЩ'
        elif role == 'полузащитник':
            role = 'ПЗЩ'
        elif role == 'вратарь':
            role = 'ВРТ'
        elif role == 'нападающий':
            role = 'НАП'
        elif role == 'центральный защитник':
            role = 'ЦЗ'
        elif role == 'левый защитник':
            role = 'ЛЗ'
        elif role == 'правый защитник':
            role = 'ПЗ'
        elif role == 'центральный полузащитник':
            role = 'ЦПЗ'
        elif role == 'левый полузащитник':
            role = 'ЛПЗ'
        elif role == 'правый полузащитник':
            role = 'ППЩ'
        else:
            role = message.text.upper()[:3]

        # режим редактирования позиции в игре
        if state_data.get('edit_role'):
            db_first_name = state_data.get('calldata_first_name')
            db_last_name = state_data.get('calldata_last_name')
            result = await edit_user(session, db_first_name, db_last_name, e_role=role)
            await show_table_player(session, user=result.id)
            await message.answer(f'{result.last_name} {result.first_name} в новом амплуа {role}')
            await state.reset_state(with_data=False)
        # режим добавления пользователя
        else:
            await state.update_data(role=role)
            await UserState.avatar.set()
            msg_cancel_editor_user = await message.answer(
                'Пришлите фотографию игрока',
                reply_markup=cancel_editor_user
            )
    else:
        msg_cancel_editor_user = await message.answer(
            'Амплуа не может содержать название команды или цифры!',
            reply_markup=cancel_editor_user
        )
    await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def avatar_user(message: Message, session, state: FSMContext):
    """
    Получение photo пользователя
    Запрос на добавление игрока в БД.
    """
    state_data = await state.get_data()

    msg_cancel_editor_user = state_data.get('msg_cancel_editor_user')
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=msg_cancel_editor_user)

    photo_url = (await message.bot.get_file(message.photo[-1].file_id)).file_path
    photo = (await message.bot.download_file(photo_url)).read()

    # режим редактирования фото
    if state_data.get('edit_avatar'):
        db_first_name = state_data.get('calldata_first_name')
        db_last_name = state_data.get('calldata_last_name')
        result = await edit_user(session, db_first_name, db_last_name, e_avatar=photo)
        avatar = InputFile(f'tgbot/services/pillow/media/player_card/{db_first_name}_{db_last_name}.png')
        await show_table_player(session, user=result.id)
        await message.answer_photo(photo=avatar,
                                   caption='Новое фото в карточке игрока')
        await state.update_data(edit_avatar=False)
        await state.reset_state(with_data=False)

    # режим добавления нового пользотателя
    else:
        first_name = state_data.get('first_name')
        last_name = state_data.get('last_name')
        middle_name = state_data.get('middle_name')
        birthday = state_data.get('birthday')
        role = state_data.get('role')
        phone = state_data.get('phone')

        await state.reset_state(with_data=False)
        msg_cancel_create_editor_user = await message.answer_photo(
            photo=photo,
            caption=f'{role} {last_name} {first_name} {middle_name} {birthday} {phone}',
            reply_markup=create_user_db
        )
        await state.update_data(photo=photo, msg_cancel_create_editor_user=msg_cancel_create_editor_user.message_id)


async def create_user(call: CallbackQuery, session, state: FSMContext):
    """Запись пользователя в БД."""
    user = await state.get_data()

    telegram_id = user.get('telegram_id')
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    middle_name = user.get('middle_name')
    birthday = user.get('birthday')
    phone = user.get('phone')
    role = user.get('role')
    photo = user.get('photo')

    new_user = await add_user(session, telegram_id, first_name, last_name, middle_name, birthday, phone, role, photo)

    await call.message.edit_reply_markup()
    await call.message.answer(new_user[0])
    # await call.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_id) НА УДАЛЕНИЕ

    if len(new_user) > 1:
        # собрать карточку игрока
        await show_table_player(session, new_user[1])

    # создание пользователя и запись о голосовании
    # poll_answer = await state.get_data()
    # if poll_answer.get('mode') == 'poll_answer' and len(new_user) > 1:
    #     if poll_answer.get('answer'):
    #         await create_users_poll(session, new_user[1], poll_answer.get('poll_id'), poll_answer.get('answer'))
    #         print(poll_answer)
    #
    await state.finish()


async def edit_or_delete_user_admin(call: CallbackQuery, session, state: FSMContext):
    """Клавиатура с пользователями для редактирования и удаления."""
    mode = call.data.split('_')[0]
    msg_cancel_editor_user = await call.message.edit_reply_markup(await team_keyboard(session, f'{mode}_'))
    await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def select_user_for_edit_admin(call: CallbackQuery, state: FSMContext):
    """Клавиатура для выбора изменения данных."""
    first_name, last_name = call.data.split('_')[1:]

    await state.update_data(calldata_first_name=first_name, calldata_last_name=last_name)
    cancel_menu_manager_user = await call.message.edit_reply_markup(mode_edit_user_keyboard)
    await state.update_data(
        calldata_first_name=first_name,
        calldata_last_name=last_name,
        cancel_menu_manager_user=cancel_menu_manager_user.message_id
    )


async def edit_credentials(call: CallbackQuery, state: FSMContext):
    """Выбор данных, которые необходимо изменить."""
    if call.data == 'first_name':
        await state.update_data(edit_first_name=True)
        await call.message.answer('Введите новое имя')
        await state.reset_state(with_data=False)
        await UserState.edit_full_name.set()
    elif call.data == 'last_name':
        await state.update_data(edit_last_name=True)
        await call.message.answer('Введите новую фамилию')
        await state.reset_state(with_data=False)
        await UserState.edit_full_name.set()
    elif call.data == 'middle_name':
        await state.update_data(edit_middle_name=True)
        await call.message.answer('Введите новое отчество')
        await state.reset_state(with_data=False)
        await UserState.edit_full_name.set()
    elif call.data == 'birthday':
        await state.update_data(edit_birthday=True)
        await call.message.answer('Введите новую дату рождения')
        await state.reset_state(with_data=False)
        await UserState.birthday.set()
    elif call.data == 'phone':
        await state.update_data(edit_phone=True)
        await call.message.answer('Введите новый номер телефона')
        await state.reset_state(with_data=False)
        await UserState.phone.set()
    elif call.data == 'avatar':
        await state.update_data(edit_avatar=True)
        await call.message.answer('Пришлите новую фотографию')
        await state.reset_state(with_data=False)
        await UserState.avatar.set()
    elif call.data == 'role':
        await state.update_data(edit_role=True)
        await call.message.answer('Введите новое амплуа')
        await state.reset_state(with_data=False)
        await UserState.role.set()
    elif call.data == 'telegram_id':
        await state.update_data(edit_telegram_id=True)
        await call.message.answer('Введите новый телеграм id')
        await state.reset_state(with_data=False)
        await UserState.telegram_id.set()
    elif call.data == 'current_club':
        await state.update_data(edit_current_club=True)
        await call.message.answer('Введите новое название клуба')
        await state.reset_state(with_data=False)
        await UserState.edit_current_club.set()


async def edit_full_name(message: Message, session, state: FSMContext):
    """Редактирование ФИО."""
    state_data = await state.get_data()
    db_first_name = state_data.get('calldata_first_name')
    db_last_name = state_data.get('calldata_last_name')
    result = None
    if state_data.get('edit_first_name'):
        result = await edit_user(session, db_first_name, db_last_name, e_first_name=message.text)
        await state.update_data(edit_first_name=False)
        await show_table_player(session, user=result.id)
    elif state_data.get('edit_last_name'):
        result = await edit_user(session, db_first_name, db_last_name, e_last_name=message.text)
        await state.update_data(edit_last_name=False)
        await show_table_player(session, user=result.id)
    elif state_data.get('edit_middle_name'):
        result = await edit_user(session, db_first_name, db_last_name, e_middle_name=message.text)
        await state.update_data(edit_middle_name=False)
        await show_table_player(session, user=result.id)
    await message.answer(f'Теперь полное имя игрока {result.last_name} {result.first_name} {result.middle_name}')
    await state.update_data(calldata_first_name=result.first_name, calldata_last_name=result.last_name)
    await state.reset_state(with_data=False)


async def edit_current_club(message: Message, session, state: FSMContext):
    """Изменение текущего клуба."""
    state_data = await state.get_data()
    db_first_name = state_data.get('calldata_first_name')
    db_last_name = state_data.get('calldata_last_name')
    current_club = message.text

    if not current_club.isdigit() and current_club not in commands:
        result = await edit_user(session, db_first_name, db_last_name, e_current_club=message.text)
        await state.update_data(edit_last_name=False)
        await show_table_player(session, user=result.id)
        await state.reset_state(with_data=False)
        await message.answer(f'{result.last_name} {result.first_name} член команды {current_club}')
    else:
        msg_cancel_editor_user = await message.answer(
            'Название клуба не может содержать название команд бота или цифры!',
            reply_markup=cancel_editor_user)
        await state.update_data(msg_cancel_editor_user=msg_cancel_editor_user.message_id)


async def cancel_user(call: CallbackQuery, state: FSMContext):
    """Отмена записи пользователя."""
    msg_cancel_create_editor_user = (await state.get_data()).get('msg_cancel_create_editor_user')
    await call.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_cancel_create_editor_user)
    await state.finish()


async def select_user_for_delete_admin(call: CallbackQuery, session, state: FSMContext):
    """Удаление пользователя."""
    first_name, last_name = call.data.split('_')[1:]
    await delete_user(session, first_name, last_name)
    await call.answer(f'Пользователь {last_name} {first_name} удален.')
    await state.finish()


async def cancel_keyboard_users(call: CallbackQuery, state: FSMContext):
    msg_cancel_editor_user = (await state.get_data()).get('msg_cancel_editor_user')
    await call.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_cancel_editor_user)
    await state.finish()


async def get_list_users(message: Message, session):
    """Получить всех пользователей."""
    users = await get_all_users(session)
    list_driver = ''

    if users:
        for i, name in enumerate(users, start=1):
            if len(list_driver) + 250 >= 4096:
                await message.answer(list_driver)
                list_driver = ''
            else:
                j = len(str(i)) * '_'
                list_driver += f'{i}____________________________________________{i}\n' \
                               f'ФИО:                    {name[1]} {name[0]} {name[2]}\n' \
                               f'Дата рождения: {name[3]}\n' \
                               f'Телефон:             {name[4]}\n' \
                               f'Телеграм id:       {name[5]}\n' \
                               f'{j}____________________________________________{j}\n'

        await message.bot.send_message(chat_id=message.bot.get('config').tg_bot.admin_ids[0], text=list_driver)
    elif not users:
        await message.bot.send_message(chat_id=message.from_user.id, text='Список пуст!')


async def cancel_create_user(call: CallbackQuery, state: FSMContext):
    msg_cancel_editor_user = (await state.get_data()).get('msg_cancel_editor_user')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=msg_cancel_editor_user)
    await state.finish()


async def cancel_menu_editor_user(call: CallbackQuery, state: FSMContext):
    cancel_menu_manager_user = (await state.get_data()).get('cancel_menu_manager_user')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=cancel_menu_manager_user)
    await state.finish()


def register_users_admin(dp: Dispatcher):
    dp.register_message_handler(users_admin, Command('user_manager'), is_admin=True)
    dp.register_callback_query_handler(cancel_menu_editor_user, text='cancel_menu_manager_user', is_admin=True)
    dp.register_callback_query_handler(add_user_admin, text='add_user', is_admin=True)
    dp.register_message_handler(telegram_id_user, state=UserState.telegram_id, is_admin=True)
    dp.register_message_handler(full_name_user, state=UserState.full_name, is_admin=True)
    dp.register_message_handler(birthday_user, state=UserState.birthday, is_admin=True)
    dp.register_message_handler(phone_user, state=UserState.phone, is_admin=True)
    dp.register_message_handler(role_user, state=UserState.role, is_admin=True)
    dp.register_message_handler(avatar_user, state=UserState.avatar, content_types='photo')
    dp.register_callback_query_handler(cancel_user, text='cancel_create_user', is_admin=True)
    dp.register_callback_query_handler(create_user, text='create_user', is_admin=True)
    dp.register_callback_query_handler(edit_or_delete_user_admin, text=['edit_user', 'delete_user'], is_admin=True)
    dp.register_callback_query_handler(select_user_for_edit_admin, mode='edit_user', is_admin=True)
    dp.register_callback_query_handler(edit_credentials, text=credentials, is_admin=True)
    dp.register_message_handler(edit_full_name, state=UserState.edit_full_name, is_admin=True)
    dp.register_message_handler(edit_current_club, state=UserState.edit_current_club, is_admin=True)
    dp.register_callback_query_handler(select_user_for_delete_admin, mode='delete_user', is_admin=True)
    dp.register_callback_query_handler(cancel_keyboard_users,
                                       text=['delete_cancel_keyboard_user', 'edit_cancel_keyboard_user'],
                                       is_admin=True)
    dp.register_message_handler(get_list_users, Command('users'), is_admin=True)
    dp.register_callback_query_handler(cancel_create_user, state=UserState, text='cancel_editor_user')
