from datetime import datetime

from db.analytics import (
    get_total_views,
    get_total_views_growth,
    get_views_growth_for_period
)

print("Всего просмотров:", get_total_views())
print("Общий прирост:", get_total_views_growth())

print(
    "Прирост за 2025-11-26:",
    get_views_growth_for_period(
        datetime(2025, 11, 26),
        datetime(2025, 11, 27)
    )
)
