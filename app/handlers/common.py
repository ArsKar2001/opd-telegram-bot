from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.db.h2db import DB
from models import User

db = DB('sqlite3db/opd-bot.sqlite')

faculties = db.get_faculties()


async def cmd_start(message: types.Message, state: FSMContext):
    user = User(message.chat.id)
    db.upset_user(user)
    await state.finish()
    await message.answer(
        text="Привет, дорогой студент. Я ОПД Бот помогу тебе разобраться с проблемами/вопросами, связанными с ОПД. "
             "Выполни команду /reg для регистрации :D",
        reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
