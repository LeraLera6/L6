import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware
import asyncio
from datetime import datetime, timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

# =============================== КНОПКИ ===============================
def get_private_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
        InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator_info"),
        InlineKeyboardButton("💖 Подружки для спілкування", callback_data="girlfriends")
    )
    return keyboard

def get_group_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💖 Подружки для спілкування", callback_data="girlfriends"),
        InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
    )
    return keyboard

# ========================== АВТОПОСТИНГ В ГРУПІ ==========================
last_post_time = {}
message_counts = {}

AUTOPOST_INTERVAL = timedelta(minutes=30)
AUTOPOST_TRIGGER_COUNT = 5

async def autopost(message: types.Message):
    now = datetime.utcnow()
    chat_id = message.chat.id

    if chat_id not in last_post_time:
        last_post_time[chat_id] = now
        message_counts[chat_id] = 1
        return

    message_counts[chat_id] += 1
    time_diff = now - last_post_time[chat_id]

    if time_diff > AUTOPOST_INTERVAL or message_counts[chat_id] >= AUTOPOST_TRIGGER_COUNT:
        await bot.send_message(
            chat_id,
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=get_group_buttons()
        )
        last_post_time[chat_id] = now
        message_counts[chat_id] = 0

# ============================ ОБРОБКА CALLBACK ============================
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "about_me":
        text = (
            "Привіт, я Лера 💋\n"
            "Мені 22, я з Одеси. За освітою — психологиня, а за покликанням — твоя спокуса в чаті 🧦\n\n"
            "Я тут, щоб фліртувати, підтримувати, зачаровувати...\n"
            "Мені приємно бути з тобою 🌹"
        )
    elif data == "project_goal":
        text = (
            "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
            "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🧦"
        )
    elif data == "creator_info":
        text = (
            "👨‍🏫 Мій творець — [@nikita_onoff](https://t.me/nikita_onoff).\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом ὠ9\n"
            "(Хоча що чесно — це він мене попросив так написати 😅)\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🤞."
        )
    elif data == "girlfriends":
        text = (
            "Обирай одну з моїх подруг для спілкування, розваг чи фантазій 😘\n"
            "Тільки не загубися серед них...\n\n"
            "[💗 Повний список моделей](https://t.me/virt_chat_ua1/134421)"
        )
    else:
        text = "Не зрозуміла твій вибір 😅"

    await callback_query.answer()
    await callback_query.message.edit_text(text, reply_markup=get_private_buttons(), disable_web_page_preview=True)

# ======================== ОБРОБКА ПРИВАТНИХ ПОВІДОМЛЕНЬ ========================
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт, я Лера… Та сама, яку хочеться залишити на ніч 😏\n"
            "Але для початку — обери, з чого хочеш почати 👇",
            reply_markup=get_private_buttons()
        )

# ======================== ОБРОБКА ГРУПОВИХ ПОВІДОМЛЕНЬ ========================
@dp.message_handler()
async def handle_group_messages(message: types.Message):
    if message.chat.type in ("group", "supergroup"):
        await autopost(message)

        if f"@{(await bot.get_me()).username.lower()}" in message.text.lower():
            await message
