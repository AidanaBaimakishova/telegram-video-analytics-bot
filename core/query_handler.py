from typing import Union

from nlp.parser import parse_query
from db.analytics import (
    get_total_views,
    get_total_likes,
    get_total_views_growth,
    get_views_growth_for_period,
)


def handle_query(text: str) -> Union[int, str]:
    """
    Обрабатывает текст пользователя и возвращает число
    """
    query = parse_query(text)

    metric = query["metric"]
    qtype = query["type"]
    period = query["period"]

    # -------- TOTAL --------
    if qtype == "total":
        if metric == "views":
            return get_total_views()
        if metric == "likes":
            return get_total_likes()

    # -------- GROWTH --------
    if qtype == "growth":
        if metric == "views":
            if period in ("today", "yesterday"):
                return get_views_growth_for_period(
                    query["start"],
                    query["end"]
                )
            else:
                return get_total_views_growth()

    return 0
