import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import os

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Получение токена из переменных среды
API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки для ЛС
private_keyboard = InlineKeyboardMarkup(row_width=1)
private_keyboard.add(
    InlineKeyboardButton("💋 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про мене", callback_data="about_lera"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🛡️ Про творця", callback_data="about_creator")
)

# Кнопка для групового чату
group_keyboard = InlineKeyboardMarkup(row_width=1)
group_keyboard.add(
    InlineKeyboardButton("💋 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("❔ Задати мені питання", url="https://t.me/LERA_V6_bot")
)

# Обработка упоминаний бота в чате
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"] and (message.reply_to_message and message.reply_to_message.from_user.username == "LERA_V6_bot" or f"@LERA_V6_bot" in message.text))
async def mentioned_in_group(message: types.Message):
    await message.reply("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=group_keyboard)

# Обработка команды /start в ЛС
@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def start_private(message: types.Message):
    await message.answer("Привіт, я Лера. Обери, що тебе цікавить нижче. ", reply_markup=private_keyboard)

# Обработка кнопки Про мене
@dp.callback_query_handler(Text(equals="about_lera"))
async def about_lera(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Мені 22, я з Одеси. Вивчала психологію і трохи магію спокуси 😉\nЛюблю бути загадкою у чаті, а в особистих можу стати тією, яку ти шукав…")
    await callback_query.answer()

# Обработка кнопки Ціль проєкту
@dp.callback_query_handler(Text(equals="project_goal"))
async def project_goal(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.")
    await callback_query.answer()

# Обработка кнопки Про творця
@dp.callback_query_handler(Text(equals="about_creator"))
async def about_creator(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Мій творець — @nikita_onoff. Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉")
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
