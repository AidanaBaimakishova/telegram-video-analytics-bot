from core.query_handler import handle_query

queries = [
    "Сколько всего просмотров?",
    "Какой прирост просмотров за вчера?",
    "Какой прирост просмотров?",
]

for q in queries:
    print(q)
    print("Ответ:", handle_query(q))
    print("-" * 40)
