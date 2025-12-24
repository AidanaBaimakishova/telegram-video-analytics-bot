from db.analytics_generic import run_aggregate

test = {
    "supported": True,
    "table": "videos",
    "aggregation": "count",
    "field": None,
    "filters": {},
    "period": "all",
}

print(run_aggregate(test))

