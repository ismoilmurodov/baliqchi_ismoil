import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import register_handlers

bot = Bot(token="7355432517:AAGkKqV35rOxW_LQ6E8kCGrwtV7Wjc9VrNY")
dp = Dispatcher(storage=MemoryStorage())


async def main():
    register_handlers(dp)

    # await set_commands(bot)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    asyncio.run(main())
