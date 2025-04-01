.
├── .env
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
│
├── data
│   ├── processed
│   └── raw
│       └── anime_rate_json.json
│
└── src
    ├── main.py
    └── bot
        ├── __init__.py
        ├── handlers
        │   ├── user_handlers.py
        │   └── __init__.py
        │
        ├── keyboards
        │   ├── user_keyboards.py
        │   └── __init__.py
        │
        └── services
            ├── data_processing.py
            ├── mal_api.py
            └── __init__.py