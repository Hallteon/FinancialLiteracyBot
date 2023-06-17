from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_stuff.models import Section, User

add_answer_callback_data = CallbackData('add_answer', 'answer')
sections_page_callback_data = CallbackData('sections_page', 'move')
delete_section_callback_data = CallbackData('delete_section', 'name')
users_page_callback_data = CallbackData('users_page', 'move')

inline_admin_panel = InlineKeyboardMarkup(row_width=2)
inline_admin_panel.add(InlineKeyboardButton(text='Создать секцию', callback_data='create_section'),
                       InlineKeyboardButton(text='Редактировать секции', callback_data='get_sections_panel'),
                       InlineKeyboardButton(text='Сделать рассылку', callback_data='create_mailing'),
                       InlineKeyboardButton(text='Пользователи бота', callback_data='get_users_panel'),
                       InlineKeyboardButton(text='Выйти', callback_data='admin_exit'))

inline_add_question_panel = InlineKeyboardMarkup(row_width=1)
inline_add_question_panel.add(InlineKeyboardButton(text='Добавить вопрос', callback_data='create_question'),
                              InlineKeyboardButton(text='Закончить редактирование секции',
                                                   callback_data='section_edit_exit'))

inline_add_answer_panel = InlineKeyboardMarkup(row_width=2)
inline_add_answer_panel.add(InlineKeyboardButton(text='Да', callback_data=add_answer_callback_data.new(answer='yes')),
                            InlineKeyboardButton(text='Нет', callback_data=add_answer_callback_data.new(answer='no')))

inline_sections_panel = InlineKeyboardMarkup(row_width=1)
inline_sections_panel.add(InlineKeyboardButton(text='Список всех секций', callback_data='get_all_sections'),
                          InlineKeyboardButton(text='Выйти', callback_data='exit_from_all_sections'))

inline_mailing_panel = InlineKeyboardMarkup(row_width=2)
inline_mailing_panel.add(InlineKeyboardButton(text='Запустить рассыку', callback_data='start_mailing'),
                         InlineKeyboardButton(text='Отменить рассылку', callback_data='cancel_mailing'))

inline_users_panel = InlineKeyboardMarkup(row_width=1)
inline_users_panel.add(InlineKeyboardButton(text='Список всех пользователей', callback_data='get_all_users'),
                       InlineKeyboardButton(text='Выйти', callback_data='exit_from_all_users'))


def generate_sections_dict():
    sections = [section.name for section in list(Section.select().execute())]
    sections_slices = [sections[i:i + 4] for i in range(0, len(sections), 4)]
    sections_dict = {}
    iterator = 1

    for sec_slice in sections_slices:
        sections_dict[iterator] = sec_slice
        iterator += 1

    return sections_dict


def generate_sections_page(page, all_pages):
    inline_sections_page = InlineKeyboardMarkup(row_width=2)

    for section in all_pages[page]:
        inline_sections_page.insert(InlineKeyboardButton(text=section, callback_data=delete_section_callback_data.new(name=section)))

    if len(all_pages) > 1:
        if page != len(all_pages) and page != 1:
            inline_sections_page.add(InlineKeyboardButton(text='Назад', callback_data=sections_page_callback_data.new(move='previous')),
                                     InlineKeyboardButton(text='Вперёд', callback_data=sections_page_callback_data.new(move='next')))

        elif page != len(all_pages):
            inline_sections_page.add(InlineKeyboardButton(text='Вперёд', callback_data=sections_page_callback_data.new(move='next')))

        elif page != 1:
            inline_sections_page.add(InlineKeyboardButton(text='Назад', callback_data=sections_page_callback_data.new(move='previous')))

    inline_sections_page.insert(InlineKeyboardButton(text='Выйти', callback_data='exit_from_all_sections'))

    return inline_sections_page


def generate_users_dict():
    users = [[user.username, user.points] for user in list(User.select().execute())]
    users_slices = [users[i:i + 100] for i in range(0, len(users), 100)]
    users_dict = {}
    iterator = 1

    for users_slice in users_slices:
        users_dict[iterator] = users_slice
        iterator += 1

    return users_dict


def generate_users_page(page, all_pages):
    inline_users_page = InlineKeyboardMarkup(row_width=2)

    users_list = ''
    iterator = -99 + page * 100

    for user in all_pages[page]:
        users_list += f'<b>{iterator}.</b> {user[0]} - {user[1]} баллов\n'
        iterator += 1

    if len(all_pages) > 1:
        if page != len(all_pages) and page != 1:
            inline_users_page.add(InlineKeyboardButton(text='Назад', callback_data=users_page_callback_data.new(move='previous')),
                                     InlineKeyboardButton(text='Вперёд', callback_data=users_page_callback_data.new(move='next')))

        elif page != len(all_pages):
            inline_users_page.add(InlineKeyboardButton(text='Вперёд', callback_data=users_page_callback_data.new(move='next')))

        elif page != 1:
            inline_users_page.add(InlineKeyboardButton(text='Назад', callback_data=users_page_callback_data.new(move='previous')))

    inline_users_page.add(InlineKeyboardButton(text='Выйти', callback_data='exit_from_all_users'))

    return users_list, inline_users_page
