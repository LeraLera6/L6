import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart

API_TOKEN = "your_bot_token_here"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- КНОПКИ ---
main_keyboard = InlineKeyboardMarkup(row_width=1)
main_keyboard.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="purpose"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")
)

# --- ОБРОБКА КОМАНД ---
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Обери, що тобі цікаво:", reply_markup=main_keyboard)

# --- ОБРОБКА КНОПОК ---
@dp.callback_query_handler(lambda c: c.data == "about_me")
async def process_about_me(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Мені 22, я з Одеси.\nВивчала психологію і трохи магію спокуси 😉\nЛюблю бути загадкою у чаті…")

@dp.callback_query_handler(lambda c: c.data == "purpose")
async def process_purpose(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку...\n"
        "**Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 💋**\n\n"
        "💬 І пам’ятай — усе це є частиною проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy) — нашого особливого Telegram-чату спокуси та фантазій.",
        parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == "creator")
async def process_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)")

@dp.callback_query_handler(lambda c: c.data == "girls")
async def process_girls(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Якщо хочеш приємно провести час онлайн — напиши одній з моїх подруг ☺️\nОсь вони: https://t.me/virt_chat_ua1/134421")

# --- ЗАПУСК ---
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
