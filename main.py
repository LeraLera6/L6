import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Глобальні змінні
last_auto_message_time = {}
GROUP_AUTO_MESSAGE_INTERVAL = timedelta(minutes=30)
TRIGGER_MESSAGE_COUNT = 5
message_counter = {}

# Кнопки для ЛС
def private_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(🤗"Хто я така?", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("🔧 Ціль проекту", callback_data="project_goal"))
    kb.add(InlineKeyboardButton("👨‍🏫 Мій творець", callback_data="about_creator"))
    kb.add(InlineKeyboardButton("💋 Мої подружки", callback_data="recommend_models"))
    return kb

# Кнопки для групи
def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💋 Обери мою подружку", callback_data="recommend_models"))
    kb.add(InlineKeyboardButton("❓Задай мені питання", url="https://t.me/LERA_V6_bot"))
    return kb

# TODO: Add handlers for commands, callbacks, group logic, etc.

if __name__ == '__main__':
    from handlers import *  # якщо є окремий файл з логікою
    executor.start_polling(dp, skip_updates=True)
