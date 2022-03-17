from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.db.h2db import DB

markings = [
    'Модули',
    'Расписание занятий',
    'Успеваемость',
    'Ответственный на факультете',
    'Про ОПД'
]

db = DB('sqlite3db/opd-bot.sqlite')

module_questions = [
    'Какой у меня сейчас модуль?',
    'Где посмотреть материалы/презентации по модулю или лекции?'
]


async def main_menu_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if not db.is_auth_user(chat_id):
        await message.answer('Это команда доступна только студентам! Введите /reg для регистрации студента!')
        return
    markup = types.ReplyKeyboardMarkup()
    markup.add(*markings)
    await message.answer('Выбери тему:', reply_markup=markup)
    await OrderMainMenu.waiting_select_theme.set()


async def select_theme(message: types.Message, state: FSMContext):
    if message.text not in markings:
        await message.answer('Пожалуйста, используйте клавиатуру ниже!')
        return
    await state.update_data(marking=message.text)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu_start, state='*', commands='main_menu')


class OrderMainMenu(StatesGroup):
    waiting_select_theme = State()
    waiting_select_module_question = State()
    waiting_select_performance_question = State()
    waiting_select_chief_faculty_question = State()
    waiting_select_about_opd_question = State()
