import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import register_handlers

bot = Bot(token="8061558107:AAFpRmaYrXQQnfsx3rq0_RIr3ksvxRzvf0k")
dp = Dispatcher(storage=MemoryStorage())


async def main():
    register_handlers(dp)

    # await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)  # Skip updates on startup
    except Exception as e:
        pass


if __name__ == "__main__":
    asyncio.run(main())
