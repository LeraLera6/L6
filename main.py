import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
import asyncio
import os
from datetime import datetime, timedelta

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# Настройки
MODEL_NAME = "gpt-4.1-mini"
CHAT_ID_LOGS = None  # можно указать ID чата логов при необходимости
AUTOPOST_INTERVAL = 1800  # 30 минут в секундах
MESSAGE_COUNT_TRIGGER = 5

# Состояние
chat_message_counts = {}
last_post_time = {}

# Кнопки
def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
        InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_question"),
        InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
    )
    return markup

# Приветствие
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = """
Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋
Можеш питати серйозне, грайливе або просто поговорити.
"""
    await message.answer(text.strip(), reply_markup=main_menu())

# Ответ на кнопку "Про творця"
@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def about_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        "👨‍🏫 Мій творець — @nikita_onoff\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
        "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶"
    )
    await bot.send_message(callback_query.from_user.id, text, parse_mode="Markdown")

# Ответ на кнопку "Задай питання"
@dp.callback_query_handler(lambda c: c.data == 'ask_question')
async def ask_question(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
        "Я використовую GPT, щоб допомогти тобі з відповідями, думками, або просто підтримати бесіду."
    )
    await bot.send_message(callback_query.from_user.id, text)

# Обработка обычных сообщений в ЛС (с AI)
@dp.message_handler(lambda message: message.chat.type == 'private')
async def gpt_response(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Ти — фліртова AI-дівчина Лера, говори ніжно, грайливо і тепло."},
                {"role": "user", "content": message.text}
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        await message.reply(reply_text)
    except Exception as e:
        await message.reply("🥺 Щось пішло не так... Спробуй пізніше.")
        logging.error(f"GPT error: {e}")

# Автопостинг в групі
@dp.message_handler(lambda message: message.chat.type in ['group', 'supergroup'])
async def handle_group_message(message: types.Message):
    chat_id = message.chat.id
    chat_message_counts[chat_id] = chat_message_counts.get(chat_id, 0) + 1

    now = datetime.utcnow()
    last_time = last_post_time.get(chat_id)

    if chat_message_counts[chat_id] >= MESSAGE_COUNT_TRIGGER or not last_time or (now - last_time).total_seconds() >= AUTOPOST_INTERVAL:
        await bot.send_message(chat_id, 
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=main_menu()
        )
        chat_message_counts[chat_id] = 0
        last_post_time[chat_id] = now

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
