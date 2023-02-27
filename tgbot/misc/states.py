from aiogram.dispatcher.filters.state import StatesGroup, State


class Tasks(StatesGroup):
    title = State()


class AboutState(StatesGroup):
    text = State()


class RulesState(StatesGroup):
    text = State()
