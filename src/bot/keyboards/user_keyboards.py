from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_kb() -> InlineKeyboardMarkup:
    """Get kb for main menu
    """
    builder = InlineKeyboardBuilder()
    builder.button(text='Найти работу', callback_data='find_job')

    return builder.as_markup()
