import pandas as pd
import pathlib
import os
import json
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class ProcessData:
    def __init__(self):
        self.root = pathlib.Path(__file__).parent.parent.parent.parent
        self.processed_data_dir = self.root / 'data' / 'processed'
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def process_anime_data(self, raw_data: json, ranking_type: str) -> pd.DataFrame:

        """
        Process raw anime data from MyAnimeList API to a DataFrame.
        Args:
            raw_data:
                Raw data from MyAnimeList API.
            ranking_type:
                Type of ranking to retrieve. Options are 'all', 'bypopularity','airing'.

        Returns: pd.DataFrame
            DataFrame containing processed anime data.
        """

        raw_data_list = []
        for anime in raw_data['data']:
            node = anime['node']

            raw_data_list.append(
                {
                    'rank':anime.get('ranking', {}).get('rank'),
                    'title':node.get('alternative_titles', {}).get('en',
                                                                   None),
                    'romaji_title':node.get('title', None),
                    'score':node.get('mean', None),
                    'popularity':node.get('num_list_users', None),
                    'release_date':node.get('start_date', None),
                    'type':str.upper(node.get('media_type', None)),
                    'episodes':node.get('num_episodes', None),
                    'pic':node.get('main_picture', {}).get('large',
                                                            'medium')
                }
            )

            raw_df_name = f"{ranking_type}_data_processed"

        df = pd.DataFrame(raw_data_list)
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['short_date'] = df['release_date'].dt.strftime("%B %Y")
        df.to_csv(self.processed_data_dir / f'{raw_df_name}.csv', index=False)
        return df

    def format_output(self, df: pd.DataFrame, ranking_type: str) -> str:
        file_path = f"{self.processed_data_dir}/{ranking_type}_data_processed.csv"
        try:
            df = pd.read_csv(file_path)
            df['popularity'] = df['popularity'].apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
        except FileNotFoundError:
            return "❌ Данные временно недоступны"

        formatted = []
        for index, row in df.head(5).iterrows():
            title = row['title'] if pd.notna(row['title']) else row['romaji_title']
            episodes = row['episodes'] if row['episodes'] != 0 else "количество неизвестно"
            formatted.append(
                f"🏆 {row['rank']} | {title} | 📅 {row['short_date']}\n\n"
                f"⭐️ Рейтинг: {row['score']} \n\n"
                f"📶 Зрители: {row['popularity']} \n\n"
                f"📺 {row['type']} | 🎬 Эпизодов: {episodes}\n\n"
                f"───────────────"
            )

        return "\n\n".join(formatted)[:4096]
