# seed.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine
from models import Product, Base

# Создаем таблицы, если их вдруг нет
Base.metadata.create_all(bind=engine)

# Получаем сессию для работы с БД
db: Session = SessionLocal()

try:
    # Очищаем таблицу перед добавлением новых данных, чтобы избежать дубликатов
    db.execute(text('TRUNCATE TABLE products RESTART IDENTITY;'))
    print("Таблица 'products' успешно очищена.")

    # --- Полный список чаев из прайса ---
    products_to_add = [
        # Зеленый чай
        Product(title="Горный туман 2022", price=20.0),
        # Белый чай
        Product(title="ТАНТРА 2023 Бай Хай Инь Жень", price=35.0),
        Product(title="ДУХ 2023 Гу Шу Бай Ча", price=38.0),
        Product(title="1000 тысяч 2024", price=70.0),
        # Улуны
        Product(title="Таоюань Габа Улун", price=20.0),
        Product(title="Владыка Старого Чая (ВЕСНА 2010)", price=24.0),
        Product(title="ОРЕХОВЫЙ Те Гуань Инь 2023", price=33.0),
        Product(title="Аромат цветов Те Гуань Инь осень 2024", price=38.0),
        # Красный чай
        Product(title="Дикий Горький Е Шен Шай Хун", price=18.0),
        Product(title="Сосновые иглы из Ай Лао", price=22.0),
        Product(title="Сливовый 2024 Е ШЕН АЙ ЛАО ХУН ЧА", price=38.0),
        Product(title="ГРУШЕВЫЙ 2021", price=46.0),
        # Шен Пуэры
        Product(title="СЛАДКИЙ ТАБАЧОК Шен Пуэр", price=22.0),
        Product(title="ПЛЕМЯ 2021 Шен Пуэр", price=22.0),
        Product(title="ВЕСЕННИЕ ПОЧКИ 2023", price=23.0),
        Product(title="Космос Гу Шу Айлао", price=28.0),
        Product(title="сон подсоЗНАНИЯ Шен Пуэр", price=40.0),
        Product(title="2400 Шен Пуэр 2022", price=140.0),
        # Шу Пуэры
        Product(title="Маденг Да Шу Ча Тоу", price=20.0),
        Product(title="Мармеладка", price=28.0),
        # Желтый чай
        Product(title="МАЙ ДИ ЧУНЬ сян 2024", price=34.0),
    ]

    # Добавляем все товары из списка в сессию
    db.add_all(products_to_add)
    # Сохраняем изменения в базе данных
    db.commit()
    print(f"Успешно добавлено {len(products_to_add)} товаров в базу данных!")

except Exception as e:
    print(f"Произошла ошибка: {e}")
    # Откатываем изменения в случае ошибки
    db.rollback()
finally:
    # Всегда закрываем сессию
    db.close()
