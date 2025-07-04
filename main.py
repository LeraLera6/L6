import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Text

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is not set. Please define it in environment variables.")

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Кнопки тільки для ЛС
main_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проекту", callback_data="project_goal"),
    InlineKeyboardButton("🛡️ Про мого творця", callback_data="creator"),
    InlineKeyboardButton("⬅️ Повернутись в чат", url="https://t.me/+d-pPVpIW-UBkZGUy")
)

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message):
    if message.chat.type == "private":
        user_name = message.from_user.first_name
        text = (f"<b>Привіт, {user_name} 😇</b>\n\n"
                "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n"
                "Хочеш ближче познайомитись зі мною або з моїми подругами? Обери, що цікаво:")
        await message.answer(text, reply_markup=main_menu)

@dp.callback_query_handler(Text(equals="about_me"))
async def callback_about_me(call: types.CallbackQuery):
    await call.message.answer("<b>Я люблю бути загадкою у чаті, але в особистих можу стати тією, яку ти хотів. 😉</b>")
    await call.answer()

@dp.callback_query_handler(Text(equals="project_goal"))
async def callback_project_goal(call: types.CallbackQuery):
    await call.message.answer(
        "<b>Ціль моєї появи проста — подарувати флірт та теплоту, презентувати моїх подружок та створити атмосферу.</b>")
    await call.answer()

@dp.callback_query_handler(Text(equals="creator"))
async def callback_creator(call: types.CallbackQuery):
    await call.message.answer(
        "<b>Мій творець — нестандартний та точний. Він любить заглядати в глибину суті ідеї і розкривати те, що інші оминають.</b>")
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
