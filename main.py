import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.exceptions import BotBlocked
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки меню
menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    InlineKeyboardButton("👩‍❤️‍👩 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🧠 Про мене", callback_data="about_me"),
    InlineKeyboardButton("👨‍💻 Про мого творця", callback_data="about_creator"),
    InlineKeyboardButton("💬 brEAst", url="https://t.me/+d-pPVpIW-UBkZGUy")
)

@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    try:
        await message.answer(
            "Привіт, я Лера 🤍\nХочеш трохи слабкої ваги?.. Обирай нижче...",
            reply_markup=menu_keyboard
        )
    except BotBlocked:
        logging.warning(f"Bot blocked by user {message.from_user.id}")

@dp.callback_query_handler(lambda c: c.data == 'about_me')
async def process_about_me(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        "Мені 22, я з Одеси.\nВивчала психологію і трохи магію спокуси 😉\nЛюблю бути загадкою у чаті..."
    )

@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def process_about_creator(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        "👨‍💻 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
