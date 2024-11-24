import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import users
from middlewares import LanguageMiddleware
from handlers import register_handlers
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from handlers.menu import router as menu_router
from handlers.orders import router as orders_router
from handlers.feedback import router as feedback_router
from handlers.settings import router as settings_router
from handlers.rooms import router as rooms_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    dp.include_router(menu_router)
    dp.include_router(orders_router)
    dp.include_router(feedback_router)
    dp.include_router(settings_router)
    dp.include_router(rooms_router)

    # await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)  # Skip updates on startup
    except Exception as e:
        pass


if __name__ == "__main__":
    asyncio.run(main())
