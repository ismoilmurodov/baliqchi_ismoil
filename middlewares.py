from aiogram.types import CallbackQuery, Message

class LanguageMiddleware:
    user_language = {}

    @staticmethod
    def get_language(user_id):
        return LanguageMiddleware.user_language.get(user_id, "uz")

    @staticmethod
    def set_language(user_id, lang):
        LanguageMiddleware.user_language[user_id] = lang
