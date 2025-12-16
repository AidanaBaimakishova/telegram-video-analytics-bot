from nlp.llm_parser import llm_parse_query

print("TEST 1:")
print(llm_parse_query("Сколько всего просмотров?"))

print("\nTEST 2:")
print(
    llm_parse_query(
        "Сколько видео у креатора с id aca1061a9d324ecf8c3fa2bb32d7be63 набрали больше 10 000 просмотров?"
    )
)
