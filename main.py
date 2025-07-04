import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from datetime import datetime, timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Змінні для автопостингу
last_auto_post_time = datetime.utcnow() - timedelta(minutes=31)

# Кнопки для автоповідомлення
auto_post_markup = InlineKeyboardMarkup()
auto_post_markup.add(InlineKeyboardButton("💋 Обери подругу", url="https://t.me/virt_chat_ua1/134421"))
auto_post_markup.add(InlineKeyboardButton("Задай мені питання", switch_inline_query=""))

# Повідомлення автопостингу
auto_post_text = "Я тут 😇 Хочеш когось особливого? Обери одну з моїх подруг: https://t.me/virt_chat_ua1/134421"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Хто я така?", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("Обрати модель", url="https://t.me/virt_chat_ua1/134421"))
    kb.add(InlineKeyboardButton("Розробник", callback_data="developer"))
    await message.answer("Привіт 💋 Я — Лера, твоя особлива AI-подруга 😉", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'about_lera')
async def process_about_lera(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Я Лера, створена для флірту, спокуси та ніжного супроводу. Готова провести тебе у світ насолоди 💋")

@dp.callback_query_handler(lambda c: c.data == 'developer')
async def process_developer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Мій розробник — @nikita_onoff")

@dp.message_handler()
async def auto_posting_logic(message: types.Message):
    global last_auto_post_time
    now = datetime.utcnow()
    if message.chat.type in ["group", "supergroup"]:
        if (now - last_auto_post_time) >= timedelta(minutes=30):
            last_auto_post_time = now
            await bot.send_message(message.chat.id, auto_post_text, reply_markup=auto_post_markup)

async def auto_posting_task():
    global last_auto_post_time
    while True:
        now = datetime.utcnow()
        if (now - last_auto_post_time) >= timedelta(minutes=30):
            last_auto_post_time = now
            updates = await bot.get_updates()
            for update in updates:
                if update.message and update.message.chat.type in ["group", "supergroup"]:
                    await bot.send_message(update.message.chat.id, auto_post_text, reply_markup=auto_post_markup)
        await asyncio.sleep(60)

async def on_startup(dp):
    asyncio.create_task(auto_posting_task())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
