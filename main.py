import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import users
from middlewares import LanguageMiddleware
from handlers import register_handlers
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    # await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)  # Skip updates on startup
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
