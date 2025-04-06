import json
import time
import logging
from pathlib import Path


class CacheManager:
    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent.parent.parent
        self.cache_data_dir = self.cache_dir / 'data' / 'raw'
        self.cache_lifetime = 3600  # 1 hour in seconds

    def get_cached_data(self, ranking_type: str) -> dict | None:
        """
        Gets cached data

        Args:
                Type of ranking to retrieve. Options are 'all', 'bypopularity','airing'.

        Returns:
            dict | None:Cache or None if outdated
        """
        cache_file = self.cache_data_dir / f'{ranking_type}_data_raw.json'

        if not cache_file.exists():
            logging.info(f"Cache not found for {ranking_type}")
            return None

        current_time = time.time()

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            if current_time - cached_data['timestamp'] > self.cache_lifetime:
                logging.info(f"Cache expired for {ranking_type}")
                return None

            logging.info(f"Using cached data for {ranking_type}")
            return cached_data['data']

        except (json.JSONDecodeError, KeyError):
            logging.error(f"Failed to read cache for {ranking_type}")
            return None

    def save_cache(self, ranking_type: str, data: dict) -> None:
        logging.info(f"Saving new cache for {ranking_type}")
        cache_file = self.cache_data_dir / f'{ranking_type}_data_raw.json'

        cache_data = {
            'timestamp': time.time(),
            'data': data
        }

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

