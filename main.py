import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Глобальні змінні ---
message_counter = {}

# --- КНОПКИ ---
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
        InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator_info"),
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="chat_models")
    )
    return keyboard

# --- CALLBACK ОБРОБКА ---
@dp.callback_query_handler(Text(startswith="about_me"))
async def cb_about_me(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Я — Лера, твоя віртуальна спокусниця та помічниця 💋\n\nМоя місія — не просто фліртувати, а створити місце, де хочеться залишитись 😈",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(Text(startswith="project_goal"))
async def cb_project_goal(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(Text(startswith="creator_info"))
async def cb_creator_info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶.",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(Text(startswith="chat_models"))
async def cb_chat_models(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.\n\n👉 https://t.me/virt_chat_ua1/134421",
        reply_markup=main_menu()
    )

# --- КОМАНДА START ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привіт, я Лера! Твоя AI-подружка для приємного флірту 🫦\n\nОбери, що хочеш дізнатися:",
        reply_markup=main_menu()
    )

# --- ГРУПОВА РОБОТА ---
@dp.message_handler(content_types=types.ContentType.TEXT)
async def group_message_handler(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        message_counter[chat_id] = message_counter.get(chat_id, 0) + 1

        if message_counter[chat_id] >= 5:
            await bot.send_message(
                chat_id,
                "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="chat_models"),
                    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
                )
            )
            message_counter[chat_id] = 0

# --- АВТОПОСТІНГ кожні 30 хв ---
async def periodic_posting():
    await bot.wait_until_ready()
    while True:
        await asyncio.sleep(1800)
        for chat_id in message_counter.keys():
            await bot.send_message(
                chat_id,
                "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="chat_models"),
                    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
                )
            )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_posting())
    executor.start_polling(dp, skip_updates=True)
