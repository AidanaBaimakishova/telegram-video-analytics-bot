Telegram Video Analytics Bot (LLM + PostgreSQL)

Project: Telegram-бот для аналитики по видео-контенту с обработкой запросов на естественном языке с помощью LLM и PostgreSQL.

Бот принимает вопросы на русском языке (например:
«Сколько всего просмотров?», «Какой прирост просмотров за вчера?»)
и возвращает точные числовые метрики, рассчитанные по данным в базе.

Возможности

- Приём запросов на естественном языке (RU)

- Использование LLM (OpenAI GPT) для парсинга запросов

- Хранение данных в PostgreSQL

- Поддержка агрегаций:

count — количество видео

sum — суммарные просмотры / лайки

- Поддержка фильтров:

по креатору (creator_id)

по диапазону дат

по условиям (больше X, меньше X)

- Telegram-интерфейс (aiogram)

 Примеры запросов

Поддерживаемые запросы:

Сколько всего видео?

Сколько всего просмотров?

Сколько всего лайков?

Какова суммарная динамика просмотров за вчерашний день?

Сколько видео у креатора с id ... за период с ... по ...?

Сколько видео набрало больше 100000 просмотров?

 Архитектура проекта
telegram-video-analytics-bot/
│
├── bot/                 # Telegram-бот (aiogram)
│   └── main.py
│
├── core/                # Бизнес-логика
│   └── query_handler.py
│
├── nlp/                 # NLP + LLM-парсер
│   ├── llm_parser.py
│   └── parser.py
│
├── db/                  # Работа с БД
│   ├── models.py
│   ├── database.py
│   ├── analytics_generic.py
│   ├── init_db.py
│   └── load_data.py
│
├── data/
│   └── videos.json      # Исходные данные
│
├── requirements.txt
├── .gitignore
└── README.md

 Как работает система

Пользователь отправляет сообщение в Telegram

Текст передаётся в LLM

LLM возвращает строгий JSON-запрос:

{
  "supported": true,
  "table": "videos",
  "aggregation": "sum",
  "field": "views_count",
  "filters": {
    "creator_id": null,
    "date_from": null,
    "date_to": null,
    "threshold": null
  }
}


Backend валидирует JSON

Генерируется SQL-запрос через SQLAlchemy

Результат возвращается пользователю в Telegram

 Структура базы данных
Таблица videos

id (UUID)

creator_id (UUID)

views_count

likes_count

comments_count

reports_count

created_at

Таблица video_snapshots

id

video_id

delta_views_count

delta_likes_count

created_at

 Установка и запуск
1 Клонирование проекта
git clone https://github.com/USERNAME/telegram-video-analytics-bot.git
cd telegram-video-analytics-bot

2 Виртуальное окружение
python -m venv venv
venv\Scripts\activate   # Windows

3 Установка зависимостей
pip install -r requirements.txt

4 Переменные окружения

Создать .env:

OPENAI_API_KEY=your_openai_key
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/video_analytics

5 Инициализация БД
python -m db.init_db

6 Загрузка данных
python -m db.load_data

7 Запуск бота
python -m bot.main

 Стек технологий

Python 3.9

PostgreSQL

SQLAlchemy

Aiogram

OpenAI GPT

Docker-ready архитектура

Clean separation: NLP / DB / Bot

 Цель проекта

Project создан для демонстрации навыков:

backend-разработки

работы с LLM

проектирования аналитических систем

интеграции Telegram-ботов

работы с SQL и PostgreSQL

 Статус проекта

 В активной разработке
Планируется:

расширение поддержки сложных запросов

кэширование

логирование запросов

Docker-сборка
