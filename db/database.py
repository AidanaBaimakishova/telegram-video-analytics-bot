from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ⚠️ ЗАМЕНИ пароль на свой
DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/video_analytics"

# Создаём engine — точку входа в БД
engine = create_engine(
    DATABASE_URL,
    echo=False  # показывает SQL-запросы в консоли (очень полезно для тестового)
)

# Фабрика сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Базовый класс для моделей
Base = declarative_base()
