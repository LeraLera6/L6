import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

# Головне меню
def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
        InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
        InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_me"),
        InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
    )
    return keyboard

# Привітальне повідомлення
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привіт, я Лера 🫦\n"
        "Твоя AI-подруга для флірту, тепла і особливих моментів. Обери кнопку нижче 👇",
        reply_markup=get_main_menu()
    )

# Обробка кнопок
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "models":
        await bot.send_message(callback_query.from_user.id,
            "У мене є подруги, які готові на більше…\n"
            "💋 Обери свою за настроєм — ось наш список:\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )

    elif data == "about_creator":
        await bot.send_message(callback_query.from_user.id,
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶",
            parse_mode="Markdown"
        )

    elif data == "ask_me":
        await bot.send_message(callback_query.from_user.id,
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )

# Обробка GPT
@dp.message_handler()
async def handle_gpt(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "Ти — фліртова AI-дівчина Лера з Одеси, ніжна, але з характером."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message['content']
        await message.reply(reply)

    except Exception as e:
        print(f"OpenAI error: {e}")
        await message.reply("
