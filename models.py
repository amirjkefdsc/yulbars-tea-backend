# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base # Импортируем наш базовый класс

# Описываем таблицу для хранения чая
class Product(Base):
    __tablename__ = 'products' # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    unit = Column(String, default='грамм')
