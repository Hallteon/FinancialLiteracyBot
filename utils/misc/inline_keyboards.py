from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

add_answer_callback_data = CallbackData('add_answer', 'answer')

inline_test_panel = InlineKeyboardMarkup(row_width=2)
inline_test_panel.add(InlineKeyboardButton(text='Создать секцию', callback_data='create_section'),
                      InlineKeyboardButton(text='Редактировать секцию', callback_data='edit_section'),
                      InlineKeyboardButton(text='Выйти', callback_data='test_panel_exit'))

# inline_section_panel = InlineKeyboardMarkup(row_width=1)
# inline_section_panel.add(InlineKeyboardButton(text='Создать первый вопрос', callback_data='create_question'))

inline_add_question_panel = InlineKeyboardMarkup(row_width=1)
inline_add_question_panel.add(InlineKeyboardButton(text='Добавить вопрос', callback_data='create_question'),
                              InlineKeyboardButton(text='Закончить редактирование секции', callback_data='section_edit_exit'))

inline_add_answer_panel = InlineKeyboardMarkup(row_width=2)
inline_add_answer_panel.add(InlineKeyboardButton(text='Да', callback_data=add_answer_callback_data.new(answer='yes')),
                            InlineKeyboardButton(text='Нет', callback_data=add_answer_callback_data.new(answer='no')))
