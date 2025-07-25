import os
import time
from datetime import datetime
from telegram import Bot

# Отримуємо токен і чат для логів з перемінних середовища
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def read_last_interaction():
    try:
        with open("ai_interactions.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
        last_block = "".join(lines[-30:])  # останні ~30 рядків
        return last_block if last_block else "Немає нових логів."
    except Exception as e:
        return f"⚠️ Не вдалося прочитати лог: {e}"

def hourly_report_loop():
    while True:
        now = datetime.now()
        if now.hour == 22 and now.minute == 30:
            try:
                log_text = read_last_interaction()
                bot.send_message(chat_id=LOG_CHAT_ID, text=f"📊 Звіт за день (22:30):\n\n{log_text}")
            except Exception as e:
                bot.send_message(chat_id=LOG_CHAT_ID, text=f"❌ Помилка при надсиланні звіту: {e}")
            time.sleep(60)  # щоб не дублювалося протягом хвилини
        time.sleep(20)  # перевірка кожні 20 сек
