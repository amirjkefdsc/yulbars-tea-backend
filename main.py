# main.py
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

# Импортируем наши модули и модели
from config import BOT_TOKEN, ADMIN_CHAT_ID
from database import engine, Base, get_db
import models

# Импортируем Bot для отправки сообщений
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties # <-- ДОБАВИТЬ ЭТОТ ИМПОРТ
from aiogram.enums import ParseMode # <-- ДОБАВИТЬ ЭТОТ ИМПОРТ

# --- Настройка ---
Base.metadata.create_all(bind=engine)
app = FastAPI()
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Адрес нашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Заменяем parse_mode=... на default=...
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # <-- ИЗМЕНИТЬ ЭТУ СТРОКУ


# --- Модели данных для валидации ---
class CartItem(BaseModel):
    id: int
    title: str
    price: float
    quantity: int

class OrderData(BaseModel):
    userId: int
    fullName: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    cartItems: List[CartItem]
    totalPrice: float
    deliveryCost: float


# --- API эндпоинты ---

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post("/api/orders")
async def create_order(order_data: OrderData, db: Session = Depends(get_db)):
    grand_total = order_data.totalPrice + order_data.deliveryCost

    # Здесь в будущем будет логика сохранения заказа в БД

    # Формируем сообщение
    order_details = ""
    for i, item in enumerate(order_data.cartItems, 1):
        order_details += f"{i}. <b>{item.title.upper()}</b>\n"
        order_details += f"   • {item.quantity} шт. × {item.price:.1f} ₽ = {item.quantity * item.price:.1f} ₽\n\n"

    message_text = f"""✨ <b>ВАШ ЗАКАЗ ОФОРМЛЕН</b> ✨
━━━━━━━━━━━━━━━━━━━━━━━━
... (вставьте сюда полный шаблон вашего сообщения) ...
━━━━━━━━━━━━━━━━━━━━━━━━
💵 <b>ИТОГО К ОПЛАТЕ: {grand_total} ₽</b>"""

    # Отправляем сообщения
    try:
        await bot.send_message(chat_id=order_data.userId, text=message_text)
        admin_message = f"✅ Новый заказ от {order_data.fullName} на сумму {grand_total} ₽."
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

    return {"status": "ok"}


# --- Запуск сервера ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
