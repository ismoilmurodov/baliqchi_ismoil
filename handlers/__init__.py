# handlers/__init__.py
from aiogram import Router
from .users import router as users_router

def register_handlers(dp: Router):
    print(13213)
    dp.include_router(users_router)
