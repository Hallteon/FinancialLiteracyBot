from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from loader import dp
from utils.db_stuff.models import User, get_all_sections_questions_data, set_user_points
from utils.misc.user_inline_keyboards import *
from states.user_states import *


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    bot_name = await dp.bot.get_me()
    user = message.from_user
    new_user = User.get_or_create(user_id=user.id, username=user.username)
    text = f"👋 <b>{user.username}, привет!\n@{bot_name.username} 🤖 - это бот, с помощью " \
           f"которого можно развивать свою финансовую грамотность 📝\n" \
           f"Введи / или отправь команду /help " \
           f"чтобы увидеть доступные команды этого бота ✅</b>"

    await message.answer(text)

    if type(new_user) != tuple:
        new_user.save()


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Доступные команды бота ✏:\n" \
           "/test - запустить тест по финансовой грамотности"

    await message.answer(text)


@dp.message_handler(Command('test'))
async def start_test(message: types.Message):
    await message.answer('<b>Меню теста:</b>', reply_markup=inline_test_panel)
    await Test.first()


@dp.callback_query_handler(text='start_test', state=Test.start)
async def start_questions(callback: types.CallbackQuery, state: FSMContext):
    questions_sections = get_all_sections_questions_data()

    async with state.proxy() as data:
        data['questions_sections'] = questions_sections
        data['current_question'] = 1
        data['current_section'] = 1

    question = questions_sections[1]['questions'][1]['question']

    await callback.message.edit_text(f'<b>Вопрос 1:</b>\n\n{question}', reply_markup=inline_question_answer)
    await Test.next()


@dp.callback_query_handler(text_contains='answer', state=Test.question)
async def answer_question(callback: types.CallbackQuery, state: FSMContext):
    answer = callback.data.split(':')[-1]

    async with state.proxy() as data:
        question = data['questions_sections'][data['current_section']]['questions'][data['current_question']]

        if (answer == 'yes' and question['answer']) or (answer == 'no' and question['answer'] == False):
            data['questions_sections'][data['current_section']]['total_points'] += question['points']

        if list(data['questions_sections'][data['current_section']]['questions'].keys())[-1] == data['current_question']:
            data['current_section'] += 1

        data['current_question'] += 1

        if data['current_section'] not in list(data['questions_sections'].keys()):
            await callback.message.edit_text('<b>Вы прошли тест, хотите узнать ваши результаты?</b>', reply_markup=inline_test_results)
            await Test.next()

        else:
            await callback.message.edit_text(f"<b>Вопрос {data['current_question']}:</b>\n\n"
                                             f"{data['questions_sections'][data['current_section']]['questions'][data['current_question']]['question']}",
                                             reply_markup=inline_question_answer)


@dp.callback_query_handler(text='get_test_results', state=Test.results)
async def get_test_results(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sections = data['questions_sections']
    total_points = 0
    results = ''

    for section_id, section in sections.items():
        total_points += section['total_points']
        results += f"<b>Секция {section_id} - \"{section['section_name']}\"</b> - <b>{section['total_points']}</b> из <b>{section['all_points']}</b> баллов;\n"

    await callback.message.edit_text(f'<b>Ваши результаты:\n</b>\n{results}\n<b>Всего набрано {total_points}</b> баллов.')

    set_user_points(callback.from_user.id, total_points)

    await state.reset_data()
    await state.reset_state()

