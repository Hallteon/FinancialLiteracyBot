from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from filters.admin_filter import IsAdmin
from loader import dp
from states.admin_states import *
from utils.db_stuff.models import Section, Question, User, delete_section_by_id
from utils.misc.admin_inline_keyboards import *


@dp.message_handler(IsAdmin(), Command('admin'))
async def send_admin_panel(message: types.Message):
    await message.answer('<b>Админ панель:</b>', reply_markup=inline_admin_panel)


@dp.callback_query_handler(text='admin_exit')
async def exit_admin_panel(callback: types.CallbackQuery):
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
    await callback.message.edit_text('<b>Напишите вопрос:</b>', reply_markup=inline_question_cancel)
    await NewSection.next()


@dp.callback_query_handler(text='cancel_create_question', state=NewSection.all_states)
async def cancel_create_question(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewSection.section_name)
    await callback.message.edit_text('<b>Выберите пункт:</b>', reply_markup=inline_add_question_panel)


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
        data['question_points'] = int(''.join(i for i in message.text if i.isdigit()))
        data['all_points'] += data['question_points']
        data['questions'].append([data['question_text'], data['question_answer'], data['question_points']])

    await state.set_state(NewSection.section_name)


@dp.callback_query_handler(text='section_edit_exit', state=NewSection.all_states)
async def get_question_all_points(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Секция успешно сохранена</b>', reply_markup=inline_admin_panel)

    data = await state.get_data()
    new_section = Section.create(name=data['section_name'], all_points=data['all_points'])

    new_section.save()

    for question in data['questions']:
        new_question = Question.create(question=question[0], answer=question[1], points=question[2])
        new_question.save()

        new_section.questions.add(Question.select().where(Question.question.contains(question[0])))

    new_section.save()

    await state.reset_data()
    await state.reset_state()


@dp.callback_query_handler(text='get_sections_panel')
async def get_sections_panel(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Выберите пункт:</b>', reply_markup=inline_sections_panel)
    await SectionsList.first()


@dp.callback_query_handler(text='get_all_sections', state=SectionsList.sections_page)
async def get_all_sections(callback: types.CallbackQuery, state: FSMContext):
    sections_dict = generate_sections_dict()
    inline_sections_page = generate_sections_page(1, sections_dict)

    await callback.message.edit_text('<b>Список всех секций (нажмите на секцию для удаления):</b>',
                                     reply_markup=inline_sections_page)

    async with state.proxy() as data:
        data['sections_pages'] = sections_dict
        data['current_page'] = 1


@dp.callback_query_handler(text_contains='sections_page', state=SectionsList.sections_page)
async def get_sections_page(callback: types.CallbackQuery, state: FSMContext):
    move = callback.data.split(':')[-1]

    async with state.proxy() as data:
        if move == 'next':
            data['current_page'] += 1

        elif move == 'previous':
            data['current_page'] -= 1

        inline_sections_page = generate_sections_page(data['current_page'], data['sections_pages'])

        await callback.message.edit_text('<b>Список всех секций (нажмите на секцию для удаления):</b>',
                                         reply_markup=inline_sections_page)


@dp.callback_query_handler(text='exit_from_all_sections', state=SectionsList.sections_page)
async def exit_from_all_sections(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_data()
    await state.reset_state()


@dp.callback_query_handler(text_contains='delete_section', state=SectionsList.sections_page)
async def delete_section(callback: types.CallbackQuery, state: FSMContext):
    section_id = callback.data.split(':')[-1]

    delete_section_by_id(section_id)
    await get_all_sections(callback, state)


@dp.callback_query_handler(text='create_mailing')
async def create_mailing(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Напишите тект рассылки:</b>')
    await Mailing.first()


@dp.message_handler(state=Mailing.mail_text)
async def get_mail_text(message: types.Message, state: FSMContext):
    await message.answer('<b>Меню рассылки:</b>', reply_markup=inline_mailing_panel)

    async with state.proxy() as data:
        data['mail_text'] = message.text

    await Mailing.next()


@dp.callback_query_handler(text='start_mailing', state=Mailing.mail_manage)
async def start_mailing(callback: types.CallbackQuery, state: FSMContext):
    users = list(User.select().execute())
    users_len = len(users)
    users_quality = len(users)
    data = await state.get_data()
    mail = data['mail_text']
    iterator = 1

    for user in users:
        await callback.message.edit_text(f'<b>Разослано {iterator} из {users_len} пользователям...</b>')

        iterator += 1

        try:
            await dp.bot.send_message(chat_id=user.id, text=mail)

        except Exception:
            users_quality -= 1
            continue

    await callback.message.edit_text(f'<b>Рассылка успешно разослана {users_quality} пользователям!</b>')
    await state.reset_data()
    await state.reset_state()


@dp.callback_query_handler(text='cancel_mailing', state=Mailing.mail_manage)
async def cancel_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('<b>Рассылка успешно отменена!</b>')
    await state.reset_data()
    await state.reset_state()


@dp.callback_query_handler(text='get_users_panel')
async def get_users_panel(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Выберите пункт:</b>', reply_markup=inline_users_panel)
    await UsersList.first()


@dp.callback_query_handler(text='exit_from_all_users', state=UsersList.users_page)
async def exit_from_all_users(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_data()
    await state.reset_state()


@dp.callback_query_handler(text='get_all_users', state=UsersList.users_page)
async def get_all_users(callback: types.CallbackQuery, state: FSMContext):
    users_dict = generate_users_dict()
    users_page = generate_users_page(1, users_dict)
    users_text_list = users_page[0]
    inline_users_page = users_page[1]

    await callback.message.edit_text(f'<b>Список всех пользователей:</b>\n{users_text_list}',
                                     reply_markup=inline_users_page)

    async with state.proxy() as data:
        data['users_pages'] = users_dict
        data['current_page'] = 1


@dp.callback_query_handler(text_contains='users_page', state=UsersList.users_page)
async def get_users_page(callback: types.CallbackQuery, state: FSMContext):
    move = callback.data.split(':')[-1]

    async with state.proxy() as data:
        if move == 'next':
            data['current_page'] += 1

        elif move == 'previous':
            data['current_page'] -= 1

        users_page = generate_users_page(data['current_page'], data['users_pages'])
        users_text_list = users_page[0]
        inline_users_page = users_page[1]

        await callback.message.edit_text(f'<b>Список всех пользователей:</b>\n{users_text_list}',
                                         reply_markup=inline_users_page)