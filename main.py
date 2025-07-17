import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
import asyncio
import os

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен и инициалицация
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- КНОПКИ ДЛЯ ЛИЧКИ (появляются под строкой ввода) ---

def private_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💞 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
        InlineKeyboardButton("Я хочу з тобою пообщаться, а ти? 🫦", callback_data="chat_start"),
        InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator_info"),
    )
    return kb

# --- Хендлер старт / приватные сообщения ---
@dp.message_handler(commands=["start"])
async def start_private(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт 😇 Я — Лера, твоя AI-подруга.

Обери кнопку нижче, щоб розпочати 😉",
            reply_markup=private_keyboard()
        )

# --- При натисканні "Я хочу з тобою пообщаться, а ти? 🫦" ---
@dp.callback_query_handler(lambda c: c.data == "chat_start")
async def start_chat_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Привіт 😇", disable_notification=True)

# --- При натисканні "Про творця" ---
@dp.callback_query_handler(lambda c: c.data == "creator_info")
async def creator_info_callback(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "👨‍🏫 Мій творець — <a href='https://t.me/nikita_onoff'>@nikita_onoff</a>
"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)

"
        "💡 Усе це — частина проєкту <a href='https://t.me/+d-pPVpIW-UBkZGUy'>brEAst</a>, "
        "створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

"
        "🤖 А ще я ожила завдяки магії <a href='https://openai.com'>OpenAI</a>. Дякую їм за це 🫶"
    )

# --- ГРУППОВАЯ ЛОГИКА ---

def group_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💞 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("Задай мені питання… 🫦", url="https://t.me/Lera_Bot_10")
    )
    return kb

@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"])
async def group_handler(message: types.Message):
    text = message.text.lower()

    if "привіт" in text or "хто тут" in text or "є хтось" in text or "напишіть мені" in text:
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Дуже хочу допомогти тобі знайти дівчат… 🫦",
            reply_markup=group_keyboard()
        )

# --- RUN ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
