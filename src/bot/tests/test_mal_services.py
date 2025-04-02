import asyncio
from src.bot.services.mal_api import MALAPIRequest
from src.bot.services.data_processing import ProcessData


async def test_anime_data_processing():

    try:
        mal_api = MALAPIRequest()
        processor = ProcessData()

        ranking_types = ['all', 'bypopularity', 'airing']

        for ranking_type in ranking_types:
            print(f"\nТестирование для {ranking_type}...")

            raw_data = await mal_api.get_anime_ranking(ranking_type=ranking_type)
            
            if raw_data is None:
                print(f"Не удалось получить данные для типа {ranking_type}")
                continue

            if 'data' not in raw_data:
                print(f"Неверная структура данных для типа {ranking_type}")
                print(f"Полученные данные: {raw_data}")
                continue

            try:
                df = processor.process_anime_data(raw_data, ranking_type)
                print(f"Количество записей: {len(df)}")
                print("Первые 3 строки данных:")
                print(df.head(3))
            except Exception as e:
                print(f"Ошибка при обработке данных: {str(e)}")

            print("-" * 50)

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_anime_data_processing())
