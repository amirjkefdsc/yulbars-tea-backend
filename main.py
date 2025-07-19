# main.py (Финальная, чистая версия)

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Импортируем наши модули и модели
from config import BOT_TOKEN, ADMIN_CHAT_ID
from database import engine, Base, get_db
import models

# Импортируем Aiogram для отправки сообщений
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# --- Настройка ---
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    # НЕ ЗАБУДЬТЕ ВСТАВИТЬ СЮДА ВАШУ РЕАЛЬНУЮ ССЫЛКУ NETLIFY
    allow_origins=["http://localhost:3000", "https://ВАША-ССЫЛКА.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация Бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# --- Модели данных для валидации ---
class CartItem(BaseModel):
    id: int
    title: str
    price: float
    grams: int

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
    """Отдает список всех товаров из БД."""
    products = db.query(models.Product).all()
    return products


@app.post("/api/orders")
async def create_order(order_data: OrderData):
    """Принимает данные заказа и отправляет уведомления."""
    grand_total = order_data.totalPrice + order_data.deliveryCost

    order_details = ""
    for i, item in enumerate(order_data.cartItems, 1):
        order_details += f"{i}. <b>{item.title.upper()}</b>\n"
        order_details += f"   • {item.grams} гр. × {item.price:.1f} ₽ = {item.grams * item.price:.1f} ₽\n\n"

    message_text = f"""✨ <b>ВАШ ЗАКАЗ ОФОРМЛЕН</b> ✨
━━━━━━━━━━━━━━━━━━━━━━━━

📋 <b>СОСТАВ ЗАКАЗА:</b>
{order_details}
━━━━━━━━━━━━━━━━━━━━━━━━
🛒 <b>СТОИМОСТЬ ТОВАРОВ:</b> {order_data.totalPrice} ₽
🚚 <b>СТОИМОСТЬ ДОСТАВКИ:</b> {order_data.deliveryCost} ₽
💵 <b>ИТОГО К ОПЛАТЕ: {grand_total} ₽</b>
━━━━━━━━━━━━━━━━━━━━━━━━

📦 <b>ИНФОРМАЦИЯ О ДОСТАВКЕ:</b>
🚚 Способ доставки: СДЭК (до пункта выдачи)
📍 Адрес: {order_data.address}
👤 Получатель: {order_data.fullName}
📞 Телефон: {order_data.phone}
━━━━━━━━━━━━━━━━━━━━━━━━

💳 <b>СУММА К ОПЛАТЕ: {grand_total} ₽</b>

Перевод на карту:
Точка Банк 🦩
<code>2204 4502 5591 4472</code>

Тинькоф 🐌
<code>2200 7007 9062 3028</code>

Сбербанк 🦔
<code>2202 2080 1895 7390</code>

<i>Комментарий к платежу не требуется</i>
━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ <b>ВАЖНО! КАК ПОДТВЕРДИТЬ ОПЛАТУ:</b>

1️⃣ Сделайте скриншот <b>ЧЕКА</b> об оплате
   (через приложение банка: "Сохранить чек")
<i>Скриншот перевода не является подтверждением</i>

2️⃣ Прикрепите чек/скриншот чека ответным сообщением на ЭТО СООББЩЕНИЕ

После подтверждения оплаты вам придет сообщение со ссылкой для отслеживания заказа

🙏🏻 Спасибо за заказ! Мы ценим ваш выбор!
"""
    try:
        await bot.send_message(chat_id=order_data.userId, text=message_text)
        admin_message = f"✅ Новый заказ от {order_data.fullName} на сумму {grand_total} ₽."
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

    return {"status": "ok"}


# --- Запуск сервера (для локальной разработки) ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
