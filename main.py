import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN is missing in environment variables")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# --- Кнопки для чату ---
chat_keyboard = InlineKeyboardMarkup(row_width=1)
chat_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про Леру", callback_data="about_lera"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🛡️ Про творця", callback_data="creator")
)

# --- Кнопки для ЛС ---
pm_keyboard = InlineKeyboardMarkup(row_width=1)
pm_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про мене", callback_data="about_lera"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🛡️ Про мого творця", callback_data="creator")
)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        text = (
            f"Привіт, {message.from_user.first_name} 😇\n\n"
            "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n"
            "Хочеш ближче познайомитись зі мною або з моїми подружками? Обери, що цікаво:"
        )
        await message.answer(text, reply_markup=pm_keyboard)

@dp.message_handler(filters.Text(equals=["Лера", "@Lera_V6_bot", "@Lera_V4bot"], ignore_case=True))
async def mention_handler(message: types.Message):
    if message.chat.type != "private":
        text = (
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
        )
        await message.reply(text, reply_markup=chat_keyboard)

@dp.callback_query_handler(lambda c: c.data == "about_lera")
async def about_lera(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Мені 22, я з Одеси. Вивчала психологію і трохи магію спокуси 😉\n"
        "Люблю бути загадкою у чаті, а в особистих можу стати тією, яку ти шукав...",
        reply_markup=pm_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "project_goal")
async def goal_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Ціль мого існування — подарувати тобі відчуття флірту, тепла, \n"
        "презентувати моделей та створити особливу атмосферу."
    )

@dp.callback_query_handler(lambda c: c.data == "creator")
async def creator_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Мій творець — @nikita_onoff. Нестандартний, точний, \n"
        "ідеаліст з добрим серцем і хітрим поглядом 😉"
    )

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
