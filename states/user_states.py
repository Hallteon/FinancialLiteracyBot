from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    start = State()
    question = State()
    results = State()