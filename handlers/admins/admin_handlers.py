from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from filters.admin_filter import IsAdmin
from loader import dp
from states.test_states import NewSection
from utils.db_stuff.models import Section, Question
from utils.misc.inline_keyboards import *


@dp.message_handler(IsAdmin(), Command('admin'))
async def send_admin_panel(message: types.Message):
    await message.answer('<b>Меню редактирования теста:</b>', reply_markup=inline_test_panel)


@dp.callback_query_handler(text='panel_exit')
async def exit_panel(callback: types.CallbackQuery):
    await callback.message.delete()


@dp.callback_query_handler(text='create_section')
async def create_section(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Напишите название новой секции:</b>')
    await NewSection.first()


@dp.message_handler(state=NewSection.section_name)
async def get_section_name(message: types.Message, state: FSMContext):
    await message.answer('<b>Выберите пункт:</b>', reply_markup=inline_add_question_panel)

    async with state.proxy() as data:
        data['section_name'] = message.text
        data['questions'] = []
        data['all_points'] = 0


@dp.callback_query_handler(text='create_question', state=NewSection.section_name)
async def get_question_text(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Напишите вопрос:</b>')
    await NewSection.next()


@dp.message_handler(state=NewSection.question_text)
async def get_question_text(message: types.Message, state: FSMContext):
    await message.answer('<b>Выберите правильный ответ:</b>', reply_markup=inline_add_answer_panel)

    async with state.proxy() as data:
        data['question_text'] = message.text

    await NewSection.next()


@dp.callback_query_handler(text_contains='add_answer', state=NewSection.question_answer)
async def get_question_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Введите количество баллов за правильный ответ:</b>')

    answer = callback.data.split(':')[-1]

    async with state.proxy() as data:
        if answer == 'yes':
            data['question_answer'] = True

        elif answer == 'no':
            data['question_answer'] = False

    await NewSection.next()


@dp.message_handler(state=NewSection.question_points)
async def get_question_points(message: types.Message, state: FSMContext):
    await message.answer('<b>Выберите для продолжения:</b>', reply_markup=inline_add_question_panel)

    async with state.proxy() as data:
        data['question_points'] = int(message.text)
        data['all_points'] += data['question_points']
        data['questions'].append([data['question_text'], data['question_answer'], data['question_points']])

    await state.set_state(NewSection.section_name)


@dp.callback_query_handler(text='section_edit_exit', state=NewSection.all_states)
async def get_question_all_points(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Секция успешно сохранена</b>')

    data = await state.get_data()
    new_section = Section.create(name=data['section_name'])

    new_section.save()

    for question in data['questions']:
        new_question = Question.create(question=question[0], answer=question[1], points=question[2])
        new_question.save()

        new_section.questions.add(Question.select().where(Question.question.contains(question[0])))

    new_section.save()

    await state.reset_data()
    await state.reset_state()

