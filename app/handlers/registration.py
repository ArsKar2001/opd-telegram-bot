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


async def select_group(call: types.CallbackQuery, state: FSMContext):
    group_id = int(call.data)

    if not db.is_group_id(group_id):
        await call.message.answer('Пожалуйста, используйте клавиатуру выше!')
        return
    user = User(call.from_user.id)
    user.group_id = group_id
    db.upset_user(user)
    await call.message.answer('Приятно познакомиться! :D Введи команду /main_menu, чтобы открыть основное меню.',
                              reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(group_id=group_id)
    await state.finish()


def register_handlers_reg(dp: Dispatcher):
    dp.register_message_handler(reg_start, state='*', commands='reg')
    dp.register_callback_query_handler(select_faculty, state=OrderStart.waiting_select_faculty)
    dp.register_callback_query_handler(select_group, state=OrderStart.waiting_select_group)


class OrderStart(StatesGroup):
    waiting_select_faculty = State()
    waiting_select_group = State()
