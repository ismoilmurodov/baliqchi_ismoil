# handlers/__init__.py
from aiogram import Router

from .feedback import router as feedback_router
from .menu import router as menu_router
from .order import router as order_router
from .order_history import router as order_history_router
from .rooms import router as rooms_router
from .settings import router as settings_router
from .users import router as users_router


def register_handlers(dp: Router):
    dp.include_router(users_router)
    dp.include_router(menu_router)
    dp.include_router(order_router)
    dp.include_router(feedback_router)
    dp.include_router(order_history_router)
    dp.include_router(settings_router)
    dp.include_router(rooms_router)
