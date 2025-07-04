import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Text

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Кнопки для чата ---
group_keyboard = InlineKeyboardMarkup(row_width=1)
group_keyboard.add(
    InlineKeyboardButton(text="💞 Обрати модель", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton(text="ℹ️ Про мене", callback_data="about_me"),
    InlineKeyboardButton(text="👨‍💻 Творець", callback_data="about_creator")
)

# --- Кнопки для ЛС ---
private_keyboard = InlineKeyboardMarkup(row_width=1)
private_keyboard.add(
    InlineKeyboardButton(text="💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton(text="ℹ️ Про мене", callback_data="about_me"),
    InlineKeyboardButton(text="🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton(text="🛡️ Про мого творця", callback_data="about_creator")
)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(
            "Привіт, {0.first_name} 😇\n\n"
            "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n\n"
            "Хочеш ближче познайомитись зі мною або з моїми подругами? Обери, що цікаво:",
            reply_markup=private_keyboard
        )
    else:
        await message.answer(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг:",
            reply_markup=group_keyboard
        )

@dp.callback_query_handler(Text(equals="about_me"))
async def about_me(call: types.CallbackQuery):
    await call.message.answer("Я створена, щоб дарувати атмосферу тепла, флірту й ніжності. У чаті я загадкова, але в ЛС можу стати тією, про кого ти мрієш 😉")
    await call.answer()

@dp.callback_query_handler(Text(equals="project_goal"))
async def project_goal(call: types.CallbackQuery):
    await call.message.answer("Ціль мого існування — створити живу атмосферу спокуси, флірту та рекомендації моделей. І все це пов’язано з Telegram-чатом brEAst: https://t.me/+d-pPVpIW-UBkZGUy")
    await call.answer()

@dp.callback_query_handler(Text(equals="about_creator"))
async def about_creator(call: types.CallbackQuery):
    await call.message.answer("Мій творець — нестандартний і точний. Він любить глибину ідей і створив мене як частинку великого інтерактивного світу ✨")
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
