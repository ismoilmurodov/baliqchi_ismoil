# handlers/__init__.py
from aiogram import Router
from .users import router as users_router
from handlers.menu import router as menu_router
from handlers.orders import router as orders_router
from handlers.feedback import router as feedback_router
from handlers.settings import router as settings_router
from handlers.rooms import router as rooms_router

def register_handlers(dp: Router):
    print(13213)
    dp.include_router(users_router)
    dp.include_router(menu_router)
    dp.include_router(orders_router)
    dp.include_router(feedback_router)
    dp.include_router(settings_router)
    dp.include_router(rooms_router)


