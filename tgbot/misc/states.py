from aiogram.dispatcher.filters.state import StatesGroup, State


class TasksState(StatesGroup):
    title = State()


class AboutState(StatesGroup):
    text = State()


class RulesState(StatesGroup):
    text = State()


class UserState(StatesGroup):
    telegram_id = State()
    full_name = State()
    birthday = State()
    role = State()
    avatar = State()
    phone = State()
    edit_full = State()
    edit_full_name = State()
    edit_current_club = State()
