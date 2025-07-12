import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# --- КНОПКИ ДЛЯ ЛС ---
menu_keyboard_private = InlineKeyboardMarkup(row_width=2)
menu_keyboard_private.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
)

# --- КНОПКИ ДЛЯ ГРУПИ ---
menu_keyboard_group = InlineKeyboardMarkup(row_width=1)
menu_keyboard_group.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
)

# --- ПЕРЕВІРКА ЧАТУ ---
is_private = lambda message: message.chat.type == "private"
is_group = lambda message: message.chat.type in ["group", "supergroup"]

# --- ОБРОБКА СТАРТУ ---
async def send_start_message(message: types.Message):
    if is_private(message):
        await message.answer("Мене звати Лера 💞\nМені 22, я з Одеси 🏖️\nЛюблю флірт, психологію та атмосферні розмови 😘", reply_markup=menu_keyboard_private)
    elif is_group(message):
        await message.answer("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=menu_keyboard_group)

# --- ОБРОБКА КНОПОК ---
async def on_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "about":
        await callback_query.message.edit_text("Мене звати Лера 💞\nМені 22, я з Одеси 🏖️\nЛюблю флірт, психологію та атмосферні розмови 😘")
    elif data == "goal":
        await callback_query.message.edit_text("🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦")
    elif data == "creator":
        await callback_query.message.edit_text("👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶.")
    elif data == "models":
        await callback_query.message.edit_text("У мене є для тебе особлива добірка моїх подруг — кожна з них чекає на твою увагу 😘\n\n🔗 Обери когось тут: https://t.me/virt_chat_ua1/134421")

    await callback_query.answer()

# --- ОСНОВНЕ ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(send_start_message, CommandStart())
dp.register_callback_query_handler(on_callback)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
