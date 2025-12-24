from nlp.llm_parser import llm_parse_query


def parse_query(text: str) -> dict:
    return llm_parse_query(text)
