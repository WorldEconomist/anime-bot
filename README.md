```
# MAL Telegram Bot  
├── .env
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
├── data/
│   └── raw/
│       ├── airing_data_raw.json
│       ├── all_data_raw.json
│       └── bypopularity_data_raw.json
└── src/
    ├── main.py
    └── bot/
        ├── __init__.py
        ├── handlers/
        │   ├── __init__.py
        │   └── user_handlers.py
        ├── keyboards/
        │   ├── __init__.py
        │   └── user_keyboards.py
        ├── services/
        │   ├── __init__.py
        │   ├── cache_manager.py
        │   ├── data_processing.py
        │   └── mal_api.py
        └── tests/
            └── test_mal_services.py
```