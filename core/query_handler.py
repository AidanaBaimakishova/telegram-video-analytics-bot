from datetime import datetime, timedelta
from nlp.parser import parse_query
from db.analytics import (
    get_total_views,
    get_total_likes,
    get_total_views_growth,
    get_views_growth_for_period,
)


def handle_query(text: str) -> int:
    print(">>> handle_query TEXT:", text)
    query = parse_query(text)
    print(">>> PARSED QUERY:", query)

    # ❗ ЕСЛИ ЗАПРОС НЕ ПОДДЕРЖИВАЕТСЯ — НЕ СЧИТАЕМ
    if not query.get("supported"):
        return 0

    metric = query.get("metric")
    qtype = query.get("type")
    period = query.get("period")

    if not metric or not qtype:
        return 0

    # TOTAL
    if qtype == "total":
        if metric == "views":
            return get_total_views()
        if metric == "likes":
            return get_total_likes()

    # GROWTH
    if qtype == "growth" and metric == "views":
        if period == "yesterday":
            end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start = end - timedelta(days=1)
            return get_views_growth_for_period(start, end)

        return get_total_views_growth()

    return 0
