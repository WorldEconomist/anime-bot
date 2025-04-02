from dotenv import load_dotenv
import os
import json
import pathlib
import aiohttp
from typing import Dict, Optional




class MALAPIRequest:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("MAL_API_TOKEN")
        self.base_url = "https://api.myanimelist.net/v2"
        self.headers = {'Authorization': f'Bearer {self.TOKEN}'}

        self.root = pathlib.Path(__file__).parent.parent.parent.parent
        self.raw_data_dir = self.root / 'data' / 'raw'
        os.makedirs(self.raw_data_dir, exist_ok=True)

    async def get_anime_ranking(self,
                                ranking_type: str = 'all',
                                limit: int = 25) -> Optional[Dict]:
        """
        Get anime ranking data from MyAnimeList API.
        Args:
            ranking_type: str
                Type of ranking to retrieve. Options are 'all', 'bypopularity','airing',
            limit: int
                Number of results to return. Default is 25.

        Returns:
            json object containing anime ranking data.
        """

        params = {
            'ranking_type': ranking_type,
            'fields': ('rank, title, mean, start_date, num_list_users,'
                       'num_episodes, media_type, alternative_titles'),
            'limit':limit
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/anime/ranking',
                                       headers = self.headers,
                                       params = params) as response:

                    if response.status != 200:
                        raise aiohttp.ClientResponseError(
                            response.request_info,
                            response.history,
                            status=response.status
                        )

                    anime_rate_raw_json = await response.json()

                    with open(self.raw_data_dir / 'anime_rate_raw_json.json',
                              'w',
                              encoding = 'utf-8') as f:
                        json.dump(anime_rate_raw_json,
                                  f,
                                  ensure_ascii=False,
                                  indent=4)
                    return anime_rate_raw_json

        except aiohttp.ClientResponseError as e:
            print(f"Http Error: {e.status}")
        except aiohttp.ClientConnectionError as e:
            print(f"Error Connecting: {e}")
        except aiohttp.ClientTimeout as e:
            print(f"Timeout Error: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")
        return None