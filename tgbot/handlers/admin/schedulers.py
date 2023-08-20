from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram_calendar_rus import simple_cal_callback, SimpleCalendar

from tgbot.keyboards.inline_statistic import statistics
from tgbot.keyboards.inline_tasks import choice_types, days_week, tasks, \
    choice_types_tasks, input_data_tasks, choice_day, types_callback, days_callback
from tgbot.misc.states import TasksState
from tgbot.services.db.query import create_users_poll, delete_user_poll, exists_polls_users, \
    get_poll_id_to_create_a_poll, \
    get_user_id_to_create_a_poll
from tgbot.services.scheduler.event_scheduler import add_jobs_in_scheduler, modify_jobs_in_scheduler
from tgbot.services.scheduler.event_scheduler import voting_scheduler
from tgbot.services.set_commands import commands


async def task_scheduler(message: Message, state: FSMContext):
    """Кнопки для выбора действия с событиями."""
    msg = await message.bot.send_message(
        chat_id=message.from_id,
        text='<b>Запланировать cобытие</b>',
        reply_markup=tasks)
    await state.update_data(
        task_mode_start=True,
        task_mode_end=True,
        msg_id_start_task=msg.message_id
    )


async def tasks_create(call: CallbackQuery, scheduler: AsyncIOScheduler, state: FSMContext):
    """
    Кнопки для выбора типа события.
    Если запланированные задачи отсутствуют, то для выбора режима
    редактирование и удаления выводится соответствуещее сообщение.
    """
    await state.update_data(сed_state=call.data)
    get_jobs = scheduler.get_jobs()
    jobs = []
    for jb in get_jobs:
        if jb.name in choice_types:
            jobs.append(jb.name)
    if len(jobs) == 4 and call.data == 'create':
        await call.answer('Установлено максимальное количество событий')
    elif not jobs and call.data == 'edit':
        await call.answer('Отсутствуют события для изменения')
    elif not jobs and call.data == 'delete':
        await call.answer('Отсутствуют события для удаления')
    else:
        await call.message.edit_reply_markup(reply_markup=choice_types_tasks)


async def type_tasks(call: CallbackQuery, callback_data: dict, scheduler: AsyncIOScheduler, state: FSMContext):
    """
    Кнопка для перехода установки конфигурации для планировщика задач scheduler
    при создании или изменении задачи
    Кнопка для выбора типа и удаления события из планировщика задач.
    """
    types_en = callback_data.get('type_name_en')
    types_ru = callback_data.get('type_name_ru')
    accusative = callback_data.get('accusative')
    await state.update_data(type_en=types_en, type_ru=types_ru)
    data = await state.get_data()
    get_jobs = scheduler.get_jobs()
    jobs, name = [], []

    for jb in get_jobs:
        if jb.name in choice_types:
            name.append(jb.name)
            jobs.append([jb.name, jb.id, jb.next_run_time])
    if data.get('сed_state') == 'create':
        if jobs and types_en not in name:
            await call.message.edit_reply_markup(reply_markup=input_data_tasks)
        elif jobs:
            for job in jobs:
                if types_en == job[0]:
                    await call.answer(f'Задача на {accusative} уже есть!')
                    await call.message.answer(
                        f'<b>Событие</b> "<i>{types_ru}</i>"\n'
                        f'<b>Cледующий запуск:</b> <i>{job[2]}</i>\n'
                    )
        else:
            await call.message.edit_reply_markup(reply_markup=input_data_tasks)
    elif data.get('сed_state') == 'edit':
        for job in jobs:
            if job[0] == types_en:
                await state.update_data(job_id=job[1])
                await call.message.edit_reply_markup(reply_markup=input_data_tasks)
            elif job[0] != types_en:
                await call.answer(f'Задача на {accusative} не установлена или удалена!')

    elif data.get('сed_state') == 'delete':
        for job in jobs:
            if job[0] == types_en:
                scheduler.remove_job(job[1])
                await call.answer(f'Задача на {accusative} успешно удалена!')
            elif job != types_en:
                await call.answer(f'Задача на {accusative} не установлена или удалена!')


async def tasks_create_title(call: CallbackQuery, state: FSMContext):
    """Кнопка для указания названия события."""
    message = await call.message.answer('<b>Введите название создаваемого события</b>')
    await state.update_data(message_id=message.message_id)
    await TasksState.title.set()


async def tasks_update_state_title(message: Message, state: FSMContext):
    """Сохранение состояния title и удаления информационного сообщения из предыдущего зендлера."""
    if message.text not in commands:
        msg_to_del = await state.get_data()
        title = message.text
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_to_del.get('message_id'))
        await state.update_data(title=title)
        await state.reset_state(with_data=False)
    else:
        await message.answer('Вы вводите текст, который cоответствует названию команды бота. '
                             'Попробуйте ещё раз..')


async def tasks_choice_day(call: CallbackQuery):
    """Кнопка для выбора дней недели."""
    await call.message.answer('<b>Выбери день недели для опроса</b>', reply_markup=choice_day)


async def tasks_update_state_day(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Кнопки с днями недели."""
    day_en = callback_data.get('day_en')
    day_ru = callback_data.get('day_ru')
    await state.update_data(day_en=day_en, day_ru=day_ru)
    await call.message.edit_reply_markup()
    await call.message.delete()


async def tasks_start_date(call: CallbackQuery, state: FSMContext):
    """
    Кнопка для выбора начальной даты и запуска календаря
    При обновлении даты для корректной работы
    стирается текущее значение
    Первично передается аргумент selected_date чтобы
    правильно отработал календарь при выборе даты
    """
    update_start_data = await state.get_data()
    if update_start_data.get('start_date'):
        await state.update_data(start_date=None)
    await state.update_data(selected_start=True)
    await call.message.edit_reply_markup(reply_markup=await SimpleCalendar().start_calendar())


async def tasks_end_date(call: CallbackQuery, state: FSMContext):
    """
    Кнопка для выбора конечной даты и запуска календаря
    При обновлении даты для корректной работы
    стирается текущее значение
    Первично передается аргумент selected_date чтобы
    правильно отработал календарь при выборе даты.
    """
    update_end_data = await state.get_data()
    if update_end_data.get('end_date'):
        await state.update_data(end_date=None)
    await state.update_data(selected_end=True)
    await call.message.edit_reply_markup(reply_markup=await SimpleCalendar().start_calendar())


async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Настройка календарей таким образом, что они вызываются каждый для своего случая
    Если вызывается нужный календарь, то ему передается True в аргументе selected_start или selected_end
    В случае, если дату календаря нужно выбрать новую, то в вызываемом хендлере tasks_start_date или
    tasks_end_date состояния выбора даты start_date или end_date изменяется на None, а здесь выполняется
    текущая проверка.
    Данный календарь используется ещё для выбора дня при получении статистики,
    поэтому тут используется переменная statistics.
    """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    data = await state.get_data()
    selected_start = data.get('selected_start', False)
    selected_end = data.get('selected_end', False)
    task_mode_start = data.get('task_mode_start', False)
    task_mode_end = data.get('task_mode_end', False)
    statistics_mode_start = data.get('statistics_mode_start', False)
    statistics_mode_end = data.get('statistics_mode_end', False)

    if selected:
        print(selected, date)
        if data.get('start_date') is None and selected_start:
            if task_mode_start:
                await state.update_data(task_mode=False)
                await callback_query.message.edit_reply_markup(reply_markup=input_data_tasks)
            elif statistics_mode_start:
                await state.update_data(statistics_mode_start=False)
                await callback_query.message.edit_reply_markup(reply_markup=statistics)
            await state.update_data(start_date=date.strftime("%Y-%m-%d"),
                                    format_start=date.strftime("%d.%m.%Y"))
        elif data.get('end_date') is None and selected_end:
            if task_mode_end:
                await state.update_data(task_mode=False)
                await callback_query.message.edit_reply_markup(reply_markup=input_data_tasks)
            elif statistics_mode_end:
                await state.update_data(statistics_mode_end=False)
                await callback_query.message.edit_reply_markup(reply_markup=statistics)
            await state.update_data(end_date=date.strftime("%Y-%m-%d"),
                                    format_end=date.strftime("%d.%m.%Y"))


async def call_task_scheduler(call: CallbackQuery, scheduler: dict, session, state: FSMContext):
    """Из state извлекаются необходимые данные для обработки
    и передачи аргументов в функцию планировщика установки задачи для add_jobs_in_scheduler или
    изменения задачи для modify_jobs_in_scheduler.
    Вывод сообщения пользователю о зарегистрированном обращении."""
    data_state = await state.get_data()
    job_id = data_state.get('job_id')
    types = data_state.get('type_ru')
    title = data_state.get('title', 'название')
    day = data_state.get('day_ru', 'день')
    format_start_date = data_state.get('format_start', 'дату начала')
    format_end_date = data_state.get('format_end', 'дату окончания')
    data = title, day, format_start_date, format_end_date
    fields = ['название', 'день', 'дату начала', 'дату окончания']
    for el in data:
        if el in fields:
            await call.message.answer(f'Необходимо выбрать {el}')
    preparation_for_start = all(el not in fields for el in data)
    if preparation_for_start and job_id is None:
        await add_jobs_in_scheduler(data_state, session, scheduler)
        await call.message.edit_reply_markup(reply_markup=choice_types_tasks)
        await call.message.answer(
            f'<b><u>Зарегистировано событие</u></b>\n'
            f'Тип события: <b>{types}</b>\n'
            f'Название: <b>{title}</b>\n'
            f'День недели: <b>{day}</b>\n'
            f'Время запуска: <b>12:00</b>\n'
            f'Планируемый период: <b>{format_start_date}-{format_end_date}</b>',
        )
    elif preparation_for_start and job_id is not None:
        await modify_jobs_in_scheduler(data_state, scheduler)
        await call.message.edit_reply_markup(reply_markup=choice_types_tasks)
        await call.message.answer(
            f'<b><u>Исправленно событие</u></b>\n'
            f'Тип события: <b>{types}</b>\n'
            f'Название: <b>{title}</b>\n'
            f'День недели: <i>{day}</b>\n'
            f'Время запуска: <b>12:00</b>\n'
            f'Планируемый период: <b>{format_start_date}-{format_end_date}</b>',
        )
    await state.reset_state(with_data=False)


async def tasks_back(call: CallbackQuery, state: FSMContext):
    """Вернуться к кнопкам выбора задач."""
    await call.message.edit_reply_markup(reply_markup=tasks)
    await state.finish()


async def types_tasks_back(call: CallbackQuery):
    """Вернуться к кнопкам выбора типа задач."""
    await call.message.edit_reply_markup(reply_markup=choice_types_tasks)


async def tasks_cancel(call: CallbackQuery, state: FSMContext):
    """Отмена по нажатию на кнопку отмена / сброс состояния пользователя."""
    msg = await state.get_data()

    await call.message.bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=msg.get('msg_id_start_task')
    )
    await state.finish()


async def poll_answer(poll: PollAnswer, session):
    """Сохранение статистики о голосованиях в БД."""
    poll_id = await get_poll_id_to_create_a_poll(session, poll.poll_id)
    user_id = await get_user_id_to_create_a_poll(session, poll.user.id)
    # print(poll_id, user_id)

    if user_id is not None:
        id_user_poll = await exists_polls_users(session, poll_id, user_id)
        if id_user_poll is not None:
            await delete_user_poll(session, id_user_poll)
        if poll.option_ids:
            await create_users_poll(session, user_id, poll_id, poll.option_ids[0])
    elif user_id is None:
        await poll.bot.send_message(
            chat_id=poll.bot.get('config').tg_bot.admin_ids[0],
            text='Голосует пользователь, которого нет в базе: '
                 f'{poll.user.id} {poll.user.full_name}\n'
                 'Добавить пользователя: /user_manager'
        )
        # await state.update_data(mode='poll_answer', poll_id=poll_id, answer=poll.option_ids[0])
        # print(poll_answer)


def register_task_admin(dp: Dispatcher):
    dp.register_message_handler(task_scheduler, Command('task_scheduler'), is_admin=True)

    dp.register_callback_query_handler(tasks_create, text=['create', 'edit', 'delete'], is_admin=True)
    dp.register_callback_query_handler(tasks_cancel, text='cancel', is_admin=True)

    dp.register_callback_query_handler(type_tasks, types_callback.filter(type_name_en=choice_types), is_admin=True)
    dp.register_callback_query_handler(tasks_back, text='back_tasks', is_admin=True)

    dp.register_callback_query_handler(tasks_create_title, text='title', is_admin=True)
    dp.register_message_handler(tasks_update_state_title, is_admin=True, state=TasksState.title)
    dp.register_callback_query_handler(tasks_choice_day, text='day', is_admin=True)
    dp.register_callback_query_handler(tasks_update_state_day, days_callback.filter(day_en=days_week), is_admin=True)
    dp.register_callback_query_handler(tasks_start_date, text='start_date', is_admin=True)
    dp.register_callback_query_handler(tasks_end_date, text='end_date', is_admin=True)
    dp.register_callback_query_handler(types_tasks_back, text='back_types', is_admin=True)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(), is_admin=True)
    dp.register_callback_query_handler(call_task_scheduler, text='continue', is_admin=True)
    # dp.register_message_handler(voting_scheduler, Command('poll'), is_admin=True)
    dp.register_poll_answer_handler(poll_answer)
