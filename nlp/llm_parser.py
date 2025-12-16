import json
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
Ты — классификатор запросов для аналитического сервиса.

Твоя задача:
определить, может ли запрос быть обработан системой.

Система поддерживает ТОЛЬКО такие запросы:
1) Итоговое количество просмотров
2) Итоговое количество лайков
3) Прирост просмотров за всё время
4) Прирост просмотров за сегодня или вчера

Запрещено:
- считать количество видео
- использовать условия (>, <, больше, меньше)
- использовать фильтры по креаторам
- использовать любые числовые пороги
- использовать группировки

Если запрос НЕ МОЖЕТ быть обработан —
верни supported=false.

Верни СТРОГО JSON без текста:

{
  "supported": true | false,
  "metric": "views" | "likes" | null,
  "type": "total" | "growth" | null,
  "period": "all" | "today" | "yesterday" | null
}

ВАЖНО:
- НИКОГДА не догадывайся
- если есть сомнения — supported=false
- не пиши пояснений
- возвращай только JSON
"""


def llm_parse_query(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )

        data = json.loads(response.choices[0].message.content)

        # ЖЁСТКАЯ ВАЛИДАЦИЯ
        if data.get("supported") is not True:
            return {"supported": False}

        if data.get("metric") not in ("views", "likes"):
            return {"supported": False}

        if data.get("type") not in ("total", "growth"):
            return {"supported": False}

        if data.get("period") not in ("all", "today", "yesterday"):
            return {"supported": False}

        return data

    except Exception as e:
        print("LLM ERROR:", e)
        return {"supported": False}
