from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_kb() -> ReplyKeyboardMarkup:
    """Get kb for main menu
    """
    kb = [
        [
            KeyboardButton(text='Самые рейтинговые онгоинги')
        ],
        [
            KeyboardButton(text='Топ по рейтингу'),
            KeyboardButton(text='Топ по популярности'),
        ],
        [
            KeyboardButton(text='Получить рекомендации')
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )

    return keyboard
