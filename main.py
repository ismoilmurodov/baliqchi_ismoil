import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    register_handlers(dp)

    await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    asyncio.run(main())
