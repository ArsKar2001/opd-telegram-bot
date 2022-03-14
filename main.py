import telebot
from telebot.types import Message

bot = telebot.TeleBot('5201118863:AAGzO3q0JxK8OJxItc0z1HrmhM_ZGV3OQH8')


@bot.message_handler(commands=['start'])
def start_handle(message: Message):
    bot.send_message(message.from_user.id, 'Запуск')


bot.polling(none_stop=True, interval=0)
