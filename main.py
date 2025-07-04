import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Text

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is not set. Please set the token in your environment variables.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Кнопки для ЛС
private_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💖 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🛡️ Про мого творця", callback_data="about_creator"),
    InlineKeyboardButton("⬅️ Повернутись в чат", url="https://t.me/+d-pPVpIW-UBkZGUy")
)

# Кнопки для групи
chat_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💖 Мої подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("❓ Задай мені питання", url="https://t.me/Lera_V6_bot")
)

# Старт у ЛС
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            f"Привіт, {message.from_user.first_name} 😇\n\n"
            "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n"
            "Обери, що цікаво — я підготувала для тебе дещо особливе:",
            reply_markup=private_buttons
        )

# Обробка callback-кнопок у ЛС
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "about_me":
        await callback_query.message.answer("Я — Лера. Та, що створена для флірту, тепла і... несподіванок 😉")
    elif data == "project_goal":
        await callback_query.message.answer("Ціль проста — подарувати тобі розрядку, інтригу і нові знайомства. Я ще у стані розробки, але дуже стараюсь.")
    elif data == "about_creator":
        await callback_query.message.answer("Мій творець — Нікіта (@nikita_onoff). Він завжди уважний до деталей і хоче, щоб тобі тут було приємно ✨")
    await callback_query.answer()

# Реакція на згадку або reply у групі
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"] and (
    (message.reply_to_message and message.reply_to_message.from_user.username == "Lera_V6_bot") or
    ("@Lera_V6_bot" in message.text)
))
async def respond_in_group(message: types.Message):
    await message.reply(
        "Ой, я тут 😇 Може, хочеш когось особливого? Або мене ближче дізнатись? Натисни:",
        reply_markup=chat_buttons
    )

# Автоповідомлення в групу кожні 30 хв
async def send_auto_message():
    await bot.send_message(
        chat_id="@virt_chat_ua1",
        text="Ой, я тут 😇 Хочеш когось особливого? Обери одну з моїх подруг або задай мені питання:",
        reply_markup=chat_buttons
    )

async def scheduler():
    while True:
        await asyncio.sleep(1800)
        await send_auto_message()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
