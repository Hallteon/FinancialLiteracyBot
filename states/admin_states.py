from aiogram.dispatcher.filters.state import StatesGroup, State


class NewSection(StatesGroup):
    section_name = State()
    question_text = State()
    question_answer = State()
    question_points = State()
    section_all_points = State()


class SectionsList(StatesGroup):
    sections_page = State()


class Mailing(StatesGroup):
    mail_text = State()
    mail_manage = State()