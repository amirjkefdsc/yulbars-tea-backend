# bot.py
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart # <-- ДОБАВИТЬ ЭТОТ ИМПОРТ
from aiogram.types import WebAppInfo

from config import BOT_TOKEN, WEBAPP_URL

# Инициализация Бота и Диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# --- Обработчики команд ---

@dp.message(CommandStart()) # <-- ИЗМЕНИТЬ ЭТУ СТРОКУ
async def send_welcome(message: types.Message):
    """Отвечает на команду /start и показывает кнопку для открытия каталога."""
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Каталог чая 🍵",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
    )
    await message.answer(
        "Добро пожаловать в наш чайный магазин! "
        "Нажмите кнопку ниже, чтобы открыть каталог.",
        reply_markup=keyboard
    )


# --- Запуск бота ---
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
