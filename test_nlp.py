from nlp.parser import parse_query

queries = [
    "Какой прирост просмотров за вчера?",
    "Сколько всего просмотров?",
    "Общее количество лайков",
]

for q in queries:
    print(q)
    print(parse_query(q))
    print("-" * 40)
