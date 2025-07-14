import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import asyncio
import os
from openai import OpenAI
from datetime import datetime

# Логування
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ініціалізація OpenAI
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Основна клавіатура
main_keyboard = InlineKeyboardMarkup(row_width=1)
main_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator"),
    InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")
)

# /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "Привіт 😘 Я Лера, твоя AI-подруга для спілкування й флірту.\n\n"
        "Обери один із варіантів нижче або просто напиши мені 💬",
        reply_markup=main_keyboard
    )

# Обробка кнопок
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "models":
        await bot.send_message(
            callback_query.from_user.id,
            "У мене є подруги, які готові на більше…\n"
            "💋 Обери свою за настроєм — ось наш список:\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )
    elif data == "ask":
        await bot.send_message(
            callback_query.from_user.id,
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )
    elif data == "creator":
        await bot.send_message(
            callback_query.from_user.id,
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶\n"
            "https://openai.com"
        )
    elif data == "skills":
        await bot.send_message(
            callback_query.from_user.id,
            "🧠 Я вмію:\n"
            "— відповідати на складні питання\n"
            "— допомагати з текстами, думками, ідеями\n"
            "— фліртувати ніжно або з вогником 😉\n"
            "— і ще багато чого — просто напиши 💬"
        )

# Відповіді AI
@dp.message_handler(lambda message: message.text and not message.text.startswith("/"))
async def ai_reply(message: types.Message):
    try:
        completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": message.text}],
            model="gpt-3.5-turbo",
        )
        response_text = completion.choices[0].message.content
        await message.reply(response_text)
    except Exception as e:
        await message.reply(f"🥺 OpenAI Error:\n{str(e)}")

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
