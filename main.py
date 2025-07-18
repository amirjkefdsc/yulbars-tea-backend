# main.py (ВРЕМЕННАЯ ВЕРСИЯ ДЛЯ НАПОЛНЕНИЯ БД)

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text

# Импортируем все необходимое
from database import SessionLocal, engine, Base
from models import Product

# ====================================================================
#           ВРЕМЕННЫЙ КОД ДЛЯ НАПОЛНЕНИЯ БАЗЫ ДАННЫХ
# ====================================================================
def seed_database():
    db: Session = SessionLocal()
    print("Запуск наполнения базы данных...")
    try:
        print("Создание таблиц...")
        Base.metadata.create_all(bind=engine)

        print("Очистка таблицы продуктов...")
        db.execute(text('TRUNCATE TABLE products RESTART IDENTITY;'))

        products_to_add = [
            Product(title="Горный туман 2022", price=20.0),
            Product(title="ТАНТРА 2023 Бай Хай Инь Жень", price=35.0),
            Product(title="ДУХ 2023 Гу Шу Бай Ча", price=38.0),
            Product(title="1000 тысяч 2024", price=70.0),
            Product(title="Таоюань Габа Улун", price=20.0),
            Product(title="Владыка Старого Чая (ВЕСНА 2010)", price=24.0),
            Product(title="ОРЕХОВЫЙ Те Гуань Инь 2023", price=33.0),
            Product(title="Аромат цветов Те Гуань Инь осень 2024", price=38.0),
            Product(title="Дикий Горький Е Шен Шай Хун", price=18.0),
            Product(title="Сосновые иглы из Ай Лао", price=22.0),
            Product(title="Сливовый 2024 Е ШЕН АЙ ЛАО ХУН ЧА", price=38.0),
            Product(title="ГРУШЕВЫЙ 2021", price=46.0),
            Product(title="СЛАДКИЙ ТАБАЧОК Шен Пуэр", price=22.0),
            Product(title="ПЛЕМЯ 2021 Шен Пуэр", price=22.0),
            Product(title="ВЕСЕННИЕ ПОЧКИ 2023", price=23.0),
            Product(title="Космос Гу Шу Айлао", price=28.0),
            Product(title="сон подсоЗНАНИЯ Шен Пуэр", price=40.0),
            Product(title="2400 Шен Пуэр 2022", price=140.0),
            Product(title="Маденг Да Шу Ча Тоу", price=20.0),
            Product(title="Мармеладка", price=28.0),
            Product(title="МАЙ ДИ ЧУНЬ сян 2024", price=34.0),
        ]

        db.add_all(products_to_add)
        db.commit()
        print(f"УСПЕШНО ДОБАВЛЕНО {len(products_to_add)} ТОВАРОВ!")
    except Exception as e:
        print(f"ПРОИЗОШЛА ОШИБКА: {e}")
        db.rollback()
    finally:
        db.close()
        print("Наполнение базы данных завершено.")

# ЗАПУСКАЕМ ФУНКЦИЮ НАПОЛНЕНИЯ ПРИ СТАРТЕ
seed_database()

# ====================================================================
#           КОНЕЦ ВРЕМЕННОГО КОДА
# ====================================================================

# Создаем приложение FastAPI, но пока не будем добавлять эндпоинты,
# чтобы сервер просто запустился, выполнил код выше и завершил работу.
app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Seeding complete. Please remove seeding code and redeploy."}
