import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import users
from middlewares import LanguageMiddleware

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni qo'shish
    dp.include_router(users.router)

    # Ishga tushirish
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
