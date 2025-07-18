# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL # Импортируем нашу строку подключения

# Создаем "движок" (engine) — основной интерфейс для связи с БД.
engine = create_engine(DATABASE_URL)

# Создаем класс SessionLocal. Экземпляры этого класса будут нашими
# индивидуальными сессиями (подключениями) к базе данных.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс `Base`. Все наши классы-модели (которые описывают таблицы)
# будут наследоваться от него.
Base = declarative_base()

# Вспомогательная функция для получения сессии БД в эндпоинтах FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
