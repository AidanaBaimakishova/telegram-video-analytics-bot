from nlp.llm_parser import llm_parse_query
print(">>> USING PARSER FROM:", __file__)


def parse_query(text: str) -> dict:
    t = text.lower()

    # ---------- RULE-BASED ----------
    if any(w in t for w in ["просмотр", "просмотры", "просмотров"]):
        if "прирост" not in t:
            return {
                "supported": True,
                "metric": "views",
                "type": "total",
                "period": "all"
            }

    if "прирост" in t and any(w in t for w in ["просмотр", "просмотры", "просмотров"]):
        if "вчера" in t:
            return {
                "supported": True,
                "metric": "views",
                "type": "growth",
                "period": "yesterday"
            }
        return {
            "supported": True,
            "metric": "views",
            "type": "growth",
            "period": "all"
        }

    if any(w in t for w in ["лайк", "лайки", "лайков"]):
        return {
            "supported": True,
            "metric": "likes",
            "type": "total",
            "period": "all"
        }

    # ---------- LLM FALLBACK ----------
    llm = llm_parse_query(text)

    if llm.get("supported"):
        return llm

    return {"supported": False}
