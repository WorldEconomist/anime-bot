import time
import json
from collections import defaultdict
from aiogram import F, types, Dispatcher, Router
from aiogram.filters import CommandStart

from bot.keyboards.user_keyboards import get_main_kb
from bot.services.data_processing import ProcessData
from bot.services.cache_manager import CacheManager
from bot.services.mal_api import MALAPIRequest

data_processor = ProcessData()
cache_manager = CacheManager()
mal_api = MALAPIRequest()

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
    raw_data = None
    ranking_type = None

    if msg.text == 'Самые рейтинговые онгоинги':
        ranking_type = 'airing'
    elif msg.text == 'Топ по рейтингу':
        ranking_type = 'all'
    elif msg.text == 'Топ по популярности':
        ranking_type = 'bypopularity'
    elif msg.text == 'Получить рекомендации':
        await msg.answer("🎯 Функция рекомендаций находится в разработке")
        return

    if ranking_type:
        try:
            raw_data = cache_manager.get_cached_data(ranking_type)
            if raw_data is None:
                raw_data = await mal_api.get_anime_ranking(ranking_type)
                if raw_data and raw_data.get('data'):
                    cache_manager.save_cache(ranking_type, raw_data)
                else:
                    await msg.answer("❌ Не удалось получить данные от API MyAnimeList")
                    return

            df = data_processor.process_anime_data(raw_data, ranking_type)
            result = data_processor.format_output(df, ranking_type)
            await msg.answer(result)
        except Exception as e:
            await msg.answer(f"❌ Произошла ошибка при обработке запроса: {str(e)}")


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

