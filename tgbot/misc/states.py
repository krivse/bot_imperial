from aiogram.dispatcher.filters.state import StatesGroup, State


class Tasks(StatesGroup):
    title = State()
