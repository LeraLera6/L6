import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from datetime import datetime
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# === КНОПКИ ===
menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
)

group_keyboard = InlineKeyboardMarkup(row_width=2)
group_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lerabreastbot")
)

# === АВТОПОСТИНГ ===
message_counter = 0

async def autopost():
    await asyncio.sleep(10)
    while True:
        await asyncio.sleep(1800)  # кожні 30 хв
        if last_chat_id:
            await send_group_post(last_chat_id)

last_chat_id = None

async def send_group_post(chat_id):
    try:
        await bot.send_message(
            chat_id,
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )
    except Exception as e:
        logging.error(f"Помилка автопостингу: {e}")

@dp.message_handler()
async def handle_all_messages(message: types.Message):
    global message_counter, last_chat_id
    if message.chat.type in ["group", "supergroup"]:
        last_chat_id = message.chat.id

        if (message.reply_to_message and message.reply_to_message.from_user.username == (await bot.me).username) \
           or f"@{(await bot.me).username.lower()}" in message.text.lower():
            await send_group_post(message.chat.id)

        message_counter += 1
        if message_counter >= 5:
            message_counter = 0
            await send_group_post(message.chat.id)

    elif message.chat.type == "private":
        text = (
            "Привіт 😘\n"
            "Я — Лера. Рада тебе бачити тут.\n"
            "Натисни одну з кнопок нижче, щоб дізнатись більше про мене 🫦"
        )
        await message.answer(text, reply_markup=menu_keyboard)

# === CALLBACK-и ===
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "about_me":
        await callback_query.message.edit_text(
            "Мені 22, я з Одеси.\n"
            "Вивчала психологію і трохи магію спокуси 😉\n"
            "Люблю бути загадкою у чаті…",
            reply_markup=menu_keyboard
        )
    elif data == "project_goal":
        await callback_query.message.edit_text(
            "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
            "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦\n\n"
            "💬 І пам’ятай — усе це є частиною проєкту brEAst — нашого особливого Telegram-чату спокуси та фантазій.",
            reply_markup=menu_keyboard
        )
    elif data == "creator":
        await callback_query.message.edit_text(
            "👨‍🏫 Мій творець — @nikita_onoff.\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)",
            reply_markup=menu_keyboard
        )
    elif data == "models":
        await callback_query.message.edit_text(
            "💞 Подружки для спілкування\n"
            "Якщо хочеш приємно провести час онлайн — напиши одній з моїх подруг 😊\n"
            "Ось вони: https://t.me/virt_chat_ua1/134421",
            reply_markup=menu_keyboard
        )
    await callback_query.answer()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(autopost())
    executor.start_polling(dp, skip_updates=True)
