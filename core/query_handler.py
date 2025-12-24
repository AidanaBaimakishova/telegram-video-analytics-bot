from nlp.parser import parse_query
from db.analytics_generic import run_aggregate


def handle_query(text: str) -> int:
    print("TELEGRAM TEXT:", text)

    parsed = parse_query(text)
    print("PARSED:", parsed)

    if not parsed.get("supported"):
        print("❌ NOT SUPPORTED")
        return 0

    result = run_aggregate(parsed)
    print("SQL RESULT:", result)

    return result

