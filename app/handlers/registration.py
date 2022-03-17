import array

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.db.h2db import DB
from models import User

db = DB('sqlite3db/opd-bot.sqlite')

faculties = db.get_faculties()

groups = db.get_groups()


async def reg_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    bb = []
    for f in faculties:
        bb.append(types.InlineKeyboardButton(text=f['name'], callback_data=f['id']))
    markup.add(*bb)
    await message.answer('Выбери свой факультет: ', reply_markup=markup)
    await OrderStart.waiting_select_faculty.set()


async def select_faculty(call: types.CallbackQuery):
    global faculties

    id = int(call.data)
    markup = types.InlineKeyboardMarkup(row_width=4)
    groups_faculty = db.find_groups_by_faculty_id(id)
    bb = []
    for g in groups_faculty:
        bb.append(types.InlineKeyboardButton(text=g['name'], callback_data=g['id']))
    markup.add(*bb)
    await OrderStart.next()
    await call.message.answer('Выбери свою группу:', reply_markup=markup)


async def select_group(call: types.CallbackQuery):
    global groups

    group_id = int(call.data)
    students = db.find_students(group_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    bb = []
    for s in students:
        bb.append(types.InlineKeyboardButton(text=s['full_name'], callback_data=s['id']))
    markup.add(*bb)
    await OrderStart.next()
    await call.message.answer('Выбери себя из списка:', reply_markup=markup)


async def select_student(call: types.CallbackQuery, state: FSMContext):
    student_id = int(call.data)
    user = User(call.from_user.id)
    user.student_id = student_id
    db.upset_user(user)
    await call.message.answer('Приятно познакомиться! :D Введи команду /main_menu, чтобы открыть основное меню.',
                              reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_reg(dp: Dispatcher):
    dp.register_message_handler(reg_start, state='*', commands='reg')
    dp.register_callback_query_handler(select_faculty, state=OrderStart.waiting_select_faculty)
    dp.register_callback_query_handler(select_group, state=OrderStart.waiting_select_group)
    dp.register_callback_query_handler(select_student, state=OrderStart.waiting_select_student)


class OrderStart(StatesGroup):
    waiting_select_faculty = State()
    waiting_select_group = State()
    waiting_select_student = State()
