from aiogram import F, types, Dispatcher, Router
from aiogram.filters import CommandStart

from bot.keyboards.user_keyboards import get_main_kb

async def cmd_start(msg: types.Message) -> None:
    """Command start

    Args:
        msg (types.Message): msg object
    """
    reply_text = (f'Привет, {msg.from_user.full_name}, чем я могу тебе помочь?\n'
                   '\n'
                   'Я могу:\n'
                   '\n'
                   '    1. Предоставить тебе информацию о топе аниме по рейтингу\n'
                   '    2. Предоставить тебе информацию о топе аниме по популярности\n'
                   '    3. Предоставить тебе топ онгоингов по рейтингу\n'
                   '    4. Порекомендовать тебе что-нибудь к просмотру\n'
                   '\n'
                   'Чего же желает твоя душа?')

    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb()
    )


async def handle_main_menu(msg: types.Message) -> None:
    """
    Args:
        msg: объект сообщения с кнопки главного меню

    Returns:
        None
    """
    await msg.answer("⏳ Обрабатываю ваш запрос...")


def register_user_handlers(dp: Dispatcher) -> None:

    router = Router()
    router.message.register(cmd_start, CommandStart())

    router.message.register(
        handle_main_menu,
        F.text.in_([
            'Самые рейтинговые онгоинги',
            'Топ по рейтингу',
            'Топ по популярности',
            'Получить рекомендации'
        ])
    )

    dp.include_router(router)
