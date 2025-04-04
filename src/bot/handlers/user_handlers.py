import time
from collections import defaultdict
from aiogram import F, types, Dispatcher, Router
from aiogram.filters import CommandStart

from bot.keyboards.user_keyboards import get_main_kb
from bot.services.data_processing import ProcessData

data_processor = ProcessData()

user_last_request = defaultdict(float)
RATE_LIMIT = 5

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
    user_id = msg.from_user.id
    current_time = time.time()

    if current_time - user_last_request[user_id] < RATE_LIMIT:
        await msg.answer("⚠️ Пожалуйста, подождите несколько секунд перед следующим запросом")
        return

    user_last_request[user_id] = current_time

    await msg.answer("⏳ Обрабатываю ваш запрос...")

    result = None
    if msg.text == 'Самые рейтинговые онгоинги':
        result = data_processor.format_output(None, 'airing')
    elif msg.text == 'Топ по рейтингу':
        result = data_processor.format_output(None, 'all')
    elif msg.text == 'Топ по популярности':
        result = data_processor.format_output(None, 'bypopularity')
    elif msg.text == 'Получить рекомендации':
        # Заглушка
        result = "🎯 Функция рекомендаций находится в разработке"

    if result:
        await msg.answer(result)
    else:
        await msg.answer("❌ Произошла ошибка при обработке запроса")


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


