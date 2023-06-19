from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


answer_callback_data = CallbackData('answer', 'variant')

inline_test_panel = InlineKeyboardMarkup(row_width=2)
inline_test_panel.add(InlineKeyboardButton(text='Начать тест', callback_data='start_test'),
                      InlineKeyboardButton(text='Моя статистика', callback_data='test_statistic'),
                      InlineKeyboardButton(text='Выйти', callback_data='exit_from_test'))

inline_question_answer = InlineKeyboardMarkup(row_width=2)
inline_question_answer.add(InlineKeyboardButton(text='Да', callback_data=answer_callback_data.new(variant='yes')),
                           InlineKeyboardButton(text='Нет', callback_data=answer_callback_data.new(variant='no')))

inline_test_results = InlineKeyboardMarkup(row_width=1)
inline_test_results.add(InlineKeyboardButton(text='Узнать результаты', callback_data='get_test_results'))

inline_test_statistic = InlineKeyboardMarkup(row_width=1)
inline_test_statistic.add(InlineKeyboardButton(text='Назад', callback_data='exit_from_statistic'))