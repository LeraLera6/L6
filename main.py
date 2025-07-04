from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Основні кнопки

def get_main_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    )
    keyboard.add(
        InlineKeyboardButton("🧠 Задай мені питання", url="https://t.me/LERA_V6_bot?start=ask")
    )
    return keyboard

# Обробка повідомлень у групі
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"])
async def handle_group_message(message: types.Message):
    if message.text and ("@LERA_V6_bot" in message.text or message.reply_to_message and message.reply_to_message.from_user.username == "LERA_V6_bot"):
        text = (
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
        )
        await message.reply(text, reply_markup=get_main_buttons())

# Привітання в ЛС
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    name = message.from_user.first_name
    text = (
        f"Привіт, {name} 😇\n"
        "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n"
        "Хочеш ближче познайомитись зі мною або з моїми подругами? Обери, що цікаво:"
    )
    await message.answer(text, reply_markup=get_main_buttons())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
