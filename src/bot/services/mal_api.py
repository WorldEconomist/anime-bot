from dotenv import load_dotenv
import os
import requests
import json
import pathlib

load_dotenv()
TOKEN = os.getenv("MAL_API_TOKEN")

url = "https://api.myanimelist.net/v2/anime/ranking"
headers = {'Authorization': f'Bearer {TOKEN}'}
params = {'ranking_type': 'all',
          'fields': 'rank, title, mean, start_date, num_list_users, num_episodes, alternative_titles',
          'limit': 25}

try:
    r = requests.get(url, params=params, headers=headers)
    anime_rate_raw_json = r.json()

except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Something went wrong:", err)

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_DIR = ROOT / 'data' / 'raw'

os.makedirs(DATA_DIR, exist_ok=True)
with open(DATA_DIR / 'anime_rate_json.json', 'w', encoding='utf-8') as f:
    json.dump(anime_rate_raw_json, f, ensure_ascii=False, indent=4)