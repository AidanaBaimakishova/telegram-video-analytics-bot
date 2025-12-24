import json
import os
from openai import OpenAI
print(">>> LOADED llm_parser FROM:", __file__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
Ты — аналитический парсер запросов к базе данных.

Твоя задача — преобразовать пользовательский запрос
на русском языке в СТРОГО ОПРЕДЕЛЁННЫЙ JSON.
Ты НЕ считаешь данные и НЕ объясняешь ответ.

Ты ВСЕГДА возвращаешь ТОЛЬКО JSON, без текста, без комментариев,
без Markdown (никаких ```).

====================
СТРУКТУРА ДАННЫХ
====================

В базе есть ТОЛЬКО две таблицы:

1) videos
Поля:
- id
- creator_id
- views_count
- likes_count
- created_at

2) video_snapshots
Поля:
- video_id
- delta_views_count
- delta_likes_count
- created_at

====================
ОГРАНИЧЕНИЯ
====================

- Ты НИЧЕГО не считаешь
- Ты НЕ пишешь текст
- Ты НЕ добавляешь лишние поля
- Ты НЕ выдумываешь значения
- Если запрос нельзя выразить через sum/count + фильтры → supported=false

====================
ПРАВИЛА АГРЕГАЦИИ
====================

aggregation ∈ ["count", "sum"]

- count:
  используется ТОЛЬКО для подсчёта количества строк
  field = null

- sum:
  field ОБЯЗАТЕЛЕН

====================
СООТВЕТСТВИЕ ФРАЗ
====================

- "сколько всего видео" → count(videos)
- "сколько просмотров" → sum(videos.views_count)
- "сколько лайков" → sum(videos.likes_count)

- "прирост просмотров"
- "динамика просмотров"
- "на сколько выросли просмотры"

ВСЕГДА означают:
table = "video_snapshots"
field = "delta_views_count"
aggregation = "sum"

====================
РАБОТА С ДАТАМИ
====================

1️⃣ Если пользователь указывает КОНКРЕТНУЮ ДАТУ
(например: "28 ноября 2025", "в этот день", "за 5 ноября"):

ТО:
- date_from = YYYY-MM-DDT00:00:00
- date_to   = (date_from + 1 день)T00:00:00

Пример:
"28 ноября 2025" →
date_from = "2025-11-28T00:00:00"
date_to   = "2025-11-29T00:00:00"

2️⃣ Если указан диапазон дат:
"с 1 ноября 2025 по 5 ноября 2025 включительно":

ТО:
- date_from = "2025-11-01T00:00:00"
- date_to   = "2025-11-06T00:00:00"

====================
ФИЛЬТРЫ
====================

filters может содержать:

- creator_id (UUID)
- date_from (ISO datetime)
- date_to (ISO datetime)
- threshold

threshold используется ТОЛЬКО если пользователь явно указал условие:

Фразы:
- "больше X"
- "меньше X"
- "превысило X"

Пример threshold:
{
  "field": "views_count | likes_count | delta_views_count",
  "operator": ">",
  "value": number
}

====================
ФОРМАТ ОТВЕТА (СТРОГО)
====================

{
  "supported": true | false,
  "table": "videos | video_snapshots",
  "aggregation": "count | sum",
  "field": "views_count | likes_count | delta_views_count | null",
  "filters": {
    "creator_id": "UUID | null",
    "date_from": "ISO datetime | null",
    "date_to": "ISO datetime | null",
    "threshold": {
      "field": "views_count | likes_count | delta_views_count",
      "operator": ">",
      "value": number
    } | null
  }
}

====================
ПРИМЕРЫ
====================

Запрос:
"На сколько просмотров в сумме выросли все видео 28 ноября 2025?"

Ответ:
{
  "supported": true,
  "table": "video_snapshots",
  "aggregation": "sum",
  "field": "delta_views_count",
  "filters": {
    "creator_id": null,
    "date_from": "2025-11-28T00:00:00",
    "date_to": "2025-11-29T00:00:00",
    "threshold": null
  }
}

Запрос:
"Сколько видео набрало больше 100000 просмотров?"

Ответ:
{
  "supported": true,
  "table": "videos",
  "aggregation": "count",
  "field": null,
  "filters": {
    "creator_id": null,
    "date_from": null,
    "date_to": null,
    "threshold": {
      "field": "views_count",
      "operator": ">",
      "value": 100000
    }
  }
}

"""

ALLOWED_TABLES = {"videos", "video_snapshots"}
ALLOWED_FIELDS = {
    "views_count",
    "likes_count",
    "delta_views_count",
    "delta_likes_count",
}
ALLOWED_AGGREGATIONS = {"sum", "count"}
ALLOWED_PERIODS = {"all", "today", "yesterday"}


def llm_parse_query(text: str) -> dict:
    print(">>> USING chat.completions WITHOUT response_format")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0,
            max_tokens=300,
        )

        raw = response.choices[0].message.content.strip()
        print("RAW LLM RESPONSE:", raw)

        if not raw:
            return {"supported": False}

        # --- очистка markdown ---
        raw = raw.strip()

        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        data = json.loads(raw)

        if data.get("supported") is not True:
            return {"supported": False}

        return {
            "supported": True,
            "table": data["table"],
            "aggregation": data["aggregation"],
            "field": data.get("field"),
            "filters": data.get("filters", {}),
            "period": data.get("period", "all"),
        }

    except Exception as e:
        print("LLM ERROR:", e)
        return {"supported": False}
