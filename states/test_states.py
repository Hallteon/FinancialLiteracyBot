from aiogram.dispatcher.filters.state import StatesGroup, State


class NewSection(StatesGroup):
    section_name = State()
    question_text = State()
    question_answer = State()
    question_points = State()
    section_all_points = State()
