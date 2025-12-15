from datetime import datetime, timedelta


def parse_query(text: str) -> dict:
    """
    Преобразует текст пользователя в структурированный запрос
    """
    text = text.lower()

    result = {
        "metric": None,   # views / likes / comments
        "type": None,     # total / growth
        "period": None,   # today / yesterday / custom
        "start": None,
        "end": None,
    }

    # ---------- МЕТРИКА ----------
    if "просмотр" in text:
        result["metric"] = "views"
    elif "лайк" in text:
        result["metric"] = "likes"
    elif "комментар" in text:
        result["metric"] = "comments"

    # ---------- ТИП ----------
    if "прирост" in text or "рост" in text:
        result["type"] = "growth"
    elif "всего" in text or "общее" in text or "сколько" in text:
        result["type"] = "total"

    # ---------- ПЕРИОД ----------
    today = datetime.now().date()

    if "вчера" in text:
        result["period"] = "yesterday"
        result["start"] = datetime.combine(today - timedelta(days=1), datetime.min.time())
        result["end"] = datetime.combine(today, datetime.min.time())

    elif "сегодня" in text:
        result["period"] = "today"
        result["start"] = datetime.combine(today, datetime.min.time())
        result["end"] = datetime.combine(today + timedelta(days=1), datetime.min.time())

    else:
        result["period"] = "all"

    return result
