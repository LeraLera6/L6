import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

last_auto_message_time = {}
GROUP_AUTO_MESSAGE_INTERVAL = timedelta(minutes=30)
message_counter = {}

def private_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🥰 Хто я така?", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("🛠 Ціль проєкту", callback_data="project_goal"))
    kb.add(InlineKeyboardButton("🙈 Мій творець", callback_data="creator_info"))
    kb.add(InlineKeyboardButton("💋 Мої подружки", callback_data="model_list"))
    return kb

def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💋 Обрати подружку", url="https://t.me/virt_chat_ua1/134421"))
    kb.add(InlineKeyboardButton("❔ Задати питання", url="https://t.me/LERA_V6_bot"))
    return kb

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_group_messages(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        cid = message.chat.id
        now = datetime.now()
        last_time = last_auto_message_time.get(cid, datetime.min)
        if now - last_time >= GROUP_AUTO_MESSAGE_INTERVAL:
            await message.answer("Я тут 😇 Хочеш когось особливого? Обери одну з моїх подруг:", reply_markup=group_buttons())
            last_auto_message_time[cid] = now

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Привіт 😘 Я Лера. Обери, з чого хочеш почати:", reply_markup=private_buttons())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
