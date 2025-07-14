import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from datetime import datetime, timedelta
import openai

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Токен и ключ API
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Переменные для автопостинга
last_post_time = datetime.now() - timedelta(minutes=30)
message_counter = 0

# Клавиатура для ЛС
private_keyboard = InlineKeyboardMarkup(row_width=1)
private_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_ai"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
)

# Клавиатура для чата
group_keyboard = InlineKeyboardMarkup(row_width=1)
group_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
)

# Обработка команды /start
@dp.message_handler(CommandStart())
async def start(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(
            "Привіт, я Лера 💋\nТвоя AI-подруга для флірту та спокуси. Обери один із варіантів нижче:",
            reply_markup=private_keyboard
        )

# Обработка callback-кнопок
@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def about_creator(callback_query: types.CallbackQuery):
    text = (
        "👨‍🏫 Мій творець — @nikita_onoff\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
        "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶"
    )
    await callback_query.message.edit_text(text, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == 'ask_ai')
async def ask_ai_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Пиши мені будь-що — я відповім як твоя AI-подруга 💋")

# Обработка обычных сообщений в ЛС
@dp.message_handler(lambda message: message.chat.type == 'private')
async def private_chat_handler(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        reply_text = response.choices[0].message['content']
        await message.answer(reply_text)
    except Exception as e:
        await message.answer("Щось пішло не так 😢 Спробуй ще раз пізніше.")
        logging.error(f"OpenAI error: {e}")

# Обработка сообщений в группе
@dp.message_handler(lambda message: message.chat.type in ['group', 'supergroup'])
async def group_handler(message: types.Message):
    global last_post_time, message_counter

    message_counter += 1

    if f"@{(await bot.get_me()).username.lower()}" in message.text.lower() or message.reply_to_message and message.reply_to_message.from_user.id == (await bot.get_me()).id:
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )
    elif datetime.now() - last_post_time >= timedelta(minutes=30) or message_counter >= 5:
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )
        message_counter = 0
        last_post_time = datetime.now()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
