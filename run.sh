#!/bin/bash

# Запускаем веб-сервер (API) в фоновом режиме
echo "Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port 10000 &

# Запускаем бота (логика команд)
echo "Starting Telegram bot polling..."
python3 bot.py
