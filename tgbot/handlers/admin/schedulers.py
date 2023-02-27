from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram_calendar_rus import simple_cal_callback, SimpleCalendar

from tgbot.keyboards.inline_tasks import choice_types, days_week, tasks, \
    choice_types_tasks, input_data_tasks, choice_day, types_callback, days_callback
from tgbot.misc.states import Tasks
from tgbot.services.scheduler.event_scheduler import add_jobs_in_scheduler, modify_jobs_in_scheduler


async def task_scheduler(message: Message):
    """Кнопки для выбора действия с событиями."""
    await message.bot.send_message(
        chat_id=message.from_id,
        text='<i>Запланировать игру / тренировку</i>',
        reply_markup=tasks)


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
    if len(jobs) == 3 and call.data == 'create':
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
    message = await call.message.answer('<i>Введи название создаваемого события</i>')
    await state.update_data(message_id=message.message_id)
    await Tasks.title.set()


async def tasks_update_state_title(message: Message, state: FSMContext):
    """Сохранение состояния title и удаления информационного сообщения из предыдущего зендлера."""
    msg_to_del = await state.get_data()
    title = message.text
    await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_to_del['message_id'])
    await state.update_data(title=title)
    await state.reset_state(with_data=False)


async def tasks_choice_day(call: CallbackQuery):
    """Кнопка для выбора дней недели."""
    await call.message.answer('<i>Выбери день недели для опроса</i>', reply_markup=choice_day)


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
    """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    data = await state.get_data()
    selected_start = data.get('selected_start', False)
    selected_end = data.get('selected_end', False)
    if selected:
        if data.get('start_date') is None and selected_start:
            await callback_query.message.edit_reply_markup(reply_markup=input_data_tasks)
            await state.update_data(start_date=date.strftime("%Y-%m-%d"),
                                    format_start=date.strftime("%d.%m.%Y"))
        elif data.get('end_date') is None and selected_end:
            await callback_query.message.edit_reply_markup(reply_markup=input_data_tasks)
            await state.update_data(end_date=date.strftime("%Y-%m-%d"),
                                    format_end=date.strftime("%d.%m.%Y"))
        await state.get_data()


async def call_task_scheduler(call: CallbackQuery, scheduler: dict, state: FSMContext):
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
        await add_jobs_in_scheduler(data_state, scheduler)
        await call.message.answer(
            f'<b><u>Зарегистировано событие</u></b>\n'
            f'<i>Тип события:</i> <i>{types}</i>\n'
            f'<i>Название:</i> <i>{title}</i>\n'
            f'<i>День недели:</i> <i>{day}</i>\n'
            f'<i>Время запуска:</i> <i>12:00</i>\n'
            f'<i>Планируемый период:</i> <i>{format_start_date}-{format_end_date}</i>')
    elif preparation_for_start and job_id is not None:
        await modify_jobs_in_scheduler(data_state, scheduler)
        await call.message.answer(
            f'<b><u>Исправленно событие</u></b>\n'
            f'\t<i>-Тип события:</i> <i>{types}</i>\n'
            f'\t<i>-Название:</i> <i>{title}</i>\n'
            f'\t<i>-День недели:</i> <i>{day}</i>\n'
            f'\t<i>-Время запуска:</i> <i>12:00</i>\n'
            f'\t<i>-Планируемый период:</i> <i>{format_start_date}-{format_end_date}</i>')


async def tasks_back(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=tasks)


async def types_tasks_back(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=choice_types_tasks)


async def tasks_cancel(call: CallbackQuery):
    await call.message.edit_reply_markup()


def register_task_admin(dp: Dispatcher):
    dp.register_message_handler(task_scheduler, Command('task_scheduler'), is_admin=True)

    dp.register_callback_query_handler(tasks_create, text=['create', 'edit', 'delete'], is_admin=True)
    dp.register_callback_query_handler(tasks_cancel, text='cancel', is_admin=True)

    dp.register_callback_query_handler(type_tasks, types_callback.filter(type_name_en=choice_types), is_admin=True)
    dp.register_callback_query_handler(tasks_back, text='back_tasks', is_admin=True)
    dp.register_callback_query_handler(tasks_cancel, text='cancel', is_admin=True)

    dp.register_callback_query_handler(tasks_create_title, text='title', is_admin=True)
    dp.register_message_handler(tasks_update_state_title, is_admin=True, state=Tasks.title)
    dp.register_callback_query_handler(tasks_choice_day, text='day', is_admin=True)
    dp.register_callback_query_handler(tasks_update_state_day, days_callback.filter(day_en=days_week), is_admin=True)
    dp.register_callback_query_handler(tasks_start_date, text='start_date', is_admin=True)
    dp.register_callback_query_handler(tasks_end_date, text='end_date', is_admin=True)
    dp.register_callback_query_handler(types_tasks_back, text='back_types', is_admin=True)
    dp.register_callback_query_handler(tasks_cancel, text='cancel', is_admin=True)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(), is_admin=True)
    dp.register_callback_query_handler(call_task_scheduler, text='continue', is_admin=True)
