from aiogram import types, Dispatcher, Router
from aiogram.filters import CommandStart

from bot.keyboards.user_keyboards import get_main_kb


async def cmd_start(msg: types.Message) -> None:
    """Command start

    Args:
        msg (types.Message): msg object
    """
    reply_text = (f'Привет, {msg.from_user.full_name}, как твои дела?\n'
                  f'Я могу помочь тебе с поиском работы!')

    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb()
    )


def register_user_handlers(dp: Dispatcher) -> None:
    """Register user handlers
    """
    router = Router()
    router.message.register(cmd_start, CommandStart())

    dp.include_router(router)
