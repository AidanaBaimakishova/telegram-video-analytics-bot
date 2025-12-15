from db.database import engine

try:
    with engine.connect() as conn:
        print("✅ Подключение к PostgreSQL успешно!")
except Exception as e:
    print("❌ Ошибка подключения:", e)
