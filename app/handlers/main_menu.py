from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.db.h2db import DB

db = DB('sqlite3db/opd-bot.sqlite')

markings = [
    'Модули',
    'Расписание занятий',
    'Успеваемость',
    'Ответственный на факультете',
    'Про ОПД'
]

questions_answers = [
    {
        'marking': 'Модули',
        'question': 'Какой у меня сейчас модуль?',
        'answer': 'Сейчас вы проходите Модуль ### у преподавателя ###'
    },
    {
        'marking': 'Модули',
        'question': 'Где посмотреть материалы/презентации по модулю или лекции?',
        'answer': 'С материалами и презентациями вы можете ознакомиться в ЭК «ОПД-1» в блоке с именованием модуля'
    },
    {
        'marking': 'Успеваемость',
        'question': 'Где посмотреть баллы по ОПД-1?',
        'answer': 'Таблица с баллами по ОПД-1 находится по ссылке ниже *ссылка*'
    },
    {
        'marking': 'Успеваемость',
        'question': 'Как выставляется оценка за контрольную точку?',
        'answer': 'Оценка за контрольную точку выставляется исходя из количества проведенных занятий и каждый год правила немного корректируются. Более подробную информацию можете уточнить у своего ответственного на факультете или в объявлениях ЭК.'
    },
    {
        'marking': 'Успеваемость',
        'question': 'Сколько баллов можно получить за модуль?',
        'answer': """Получить баллы за модуль можно:
                1. За посещение занятий, за каждое из которых даётся по 2 балла (16 занятий – 32 балла). За 5 модуль можно получить max 4 балла
                2. За активность во время пары (за каждый модуль можно получить max 3 балла: 4 модуля – 12 баллов)
                3. За прохождения теста по окончанию модуля, за который можно получить до 8 баллов (4 теста – 32 балла
                4. Индивидуальное задание (тест) (max 20 баллов)"""
    },
    {
        'marking': 'Успеваемость',
        'question': 'Как выставляется оценка на сессии?',
        'answer': """Если в общей сумме за семестр Вы набрали больше 60 баллов, то получаете зачет «автоматом» Если же Вы не сумели набрать 60 баллов, то Вам необходимо явиться на устный зачёт, который будет проходить согласно расписанию в период сессии (вопросы для подготовки к устному зачету будут размещены в ЭК)"""
    },
    {
        'marking': 'Про ОПД',
        'question': 'Что такое ОПД?',
        'answer': """ОПД – это курс, который содержит основную информацию в области проектной деятельности, которая сможет послужить базой для реализации собственного проекта, как в составе проектной команды, так и индивидуального."""
    },
    {
        'marking': 'Про ОПД',
        'question': 'Каковы цель и задачи дисциплины?',
        'answer': """Цель дисциплины - приобретение студентами компетенций в области проектной деятельности и реализации проекта.
            Задачи дисциплины:
            I. приобретение студентами навыков формирования и работы в команде;
            II. развитие у студентов лидерских качеств;
            III. выстраивание индивидуальной образовательной траектории студента;
            IV. приобретение студентами навыков постановки и разделения задач внутри команды, определение ролей и планирования;
            V. развитие у студентов системного, аналитического и критического мышления;
            VI. создание студенческих мультикоманд для дальнейшей реализации проектов в рамках технологии ГПО;
            VII. развитие практико-ориентированного подхода в образовании;
            VIII. приобретение студентами профильных и надпрофильных навыков в области формируемых дисциплиной компетенции."""
    },
    {
        'marking': 'Про ОПД',
        'question': 'Группа по дисциплине ОПД в ВКонтакте',
        'answer': """https://vk.com/opd_tusur"""
    },
    {
        'marking': 'Расписание занятий',
        'question': 'Где я могу знать свое расписание по ОПД1?',
        'answer': """Свое расписание можно узнать на официальном портале университета:  https://timetable.tusur.ru"""
    }
]


async def main_menu_start(message: types.Message):
    chat_id = message.chat.id
    if not db.is_auth_user(chat_id):
        await message.answer('Это команда доступна только студентам! Введите /reg для регистрации студента!')
        return
    markup = types.ReplyKeyboardMarkup()
    markup.add(*markings)
    await message.answer('Выбери тему:', reply_markup=markup)
    await OrderMainMenu.waiting_select_marking.set()


async def select_marking(message: types.Message, state: FSMContext):
    if message.text not in markings:
        await message.answer('Пожалуйста, используйте клавиатуру ниже!')
        return
    marking = message.text
    await state.update_data(marking=marking)

    markup = types.ReplyKeyboardMarkup()
    for qa in questions_answers:
        if qa['marking'] == marking:
            markup.row(types.KeyboardButton(text=qa['question']))
    markup.row(types.KeyboardButton(text='Назад'))
    await message.answer(f'Вопросы по блоку \"{marking}\":', reply_markup=markup)
    await OrderMainMenu.waiting_select_question.set()


def check_qa(text, field):
    global questions_answers
    for qa in questions_answers:
        if qa[field] == text:
            return True
    return False


def get_answer_the_question(question):
    for qa in questions_answers:
        if qa['question'] == question:
            return qa['answer']
    return None


async def select_question(message: types.Message, state: FSMContext):
    if not check_qa(message.text, 'question'):
        await message.answer('Пожалуйста, используйте клавиатуру ниже!')
        return
    question = message.text
    answer_the_question = get_answer_the_question(question)
    await message.reply(answer_the_question)


async def cancel(message: types.Message):
    await OrderMainMenu.waiting_select_marking.set()
    await main_menu_start(message)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu_start, state='*', commands='main_menu')
    dp.register_message_handler(cancel, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(select_marking, state=OrderMainMenu.waiting_select_marking)
    dp.register_message_handler(select_question, state=OrderMainMenu.waiting_select_question)


class OrderMainMenu(StatesGroup):
    waiting_select_marking = State()
    waiting_select_question = State()
