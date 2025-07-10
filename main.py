import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.middlewares import BaseMiddleware

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- КНОПКИ ДЛЯ ЛС ---
menu_keyboard_private = InlineKeyboardMarkup(row_width=2)
menu_keyboard_private.add(
    InlineKeyboardButton(text="👥 Про мене", callback_data="about"),
    InlineKeyboardButton(text="🧠 Ціль проєкту", callback_data="purpose"),
    InlineKeyboardButton(text="🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton(text="💞 Подружки для спілкування", callback_data="models")
)

# --- КНОПКИ ДЛЯ ГРУПИ ---
menu_keyboard_group = InlineKeyboardMarkup(row_width=2)
menu_keyboard_group.add(
    InlineKeyboardButton(text="💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton(text="❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
)

# --- ПЕРЕВІРКА ПРИВАТНОГО ЧАТУ ---
def is_private(message: types.Message) -> bool:
    return message.chat.type == types.ChatType.PRIVATE

# --- ПЕРЕВІРКА ГРУПИ ---
def is_group(message: types.Message) -> bool:
    return message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]

# --- ПРИВІТАННЯ В ЛС ---
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    if is_private(message):
        await message.answer("Привіт, я Лера 🤍\nОберіть один із варіантів нижче:", reply_markup=menu_keyboard_private)

# --- ОБРОБКА CALLBACK-КНОПОК В ЛС ---
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "about":
        text = "Я — AI-дівчина, створена для спокуси, флірту і тепла 💋\nТрохи загадкова... але щира.\nНапиши мені, якщо хочеш ближче познайомитись 😉"
    elif data == "purpose":
        text = "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦"
    elif data == "creator":
        text = "👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶."
    elif data == "models":
        text = "Обери одну з моїх подруг для особливого спілкування 💕\nПовний список тут 👉 https://t.me/virt_chat_ua1/134421"
    else:
        text = "Хмм... щось пішло не так. Спробуй ще раз."
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text)

# --- РЕАКЦІЯ НА ЗГАДКУ В ГРУПІ ---
@dp.message_handler(lambda message: is_group(message) and ("@Lera_V4bot" in message.text or message.reply_to_message and message.reply_to_message.from_user.username == "Lera_V4bot"))
async def mentioned_in_group(message: types.Message):
    text = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
    await message.reply(text, reply_markup=menu_keyboard_group)

# --- СТАРТ БОТА ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
