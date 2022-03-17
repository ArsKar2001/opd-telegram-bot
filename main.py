import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.handlers.common import register_handlers_common
from app.handlers.main_menu import register_handlers_main_menu
from app.handlers.registration import register_handlers_reg


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск"),
        BotCommand(command="/reg", description="Зарегистрироваться"),
        BotCommand(command="/cancel", description="Отменить"),
        BotCommand(command="/main_menu", description="Вызов основого меню")
    ]
    await bot.set_my_commands(commands)


async def main():
    token = getenv('OPD_BOT_TOKEN')

    if not token:
        exit("Error: no token provided")

    bot = Bot(token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    await set_commands(bot)

    # Регистрация обработчиков
    register_handlers_common(dp)
    register_handlers_reg(dp)
    register_handlers_main_menu(dp)

    # Запуск бота
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
