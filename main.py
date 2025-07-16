from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import logging
import os

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
        InlineKeyboardButton("💬 Задай мені питання 😗", callback_data="ask_me"),
        InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
    )
    await message.answer("Привіт, я дуже хочу допомогти тобі знайти справжніх дівчат для спілкування 💋", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "ask_me")
async def handle_ask_me(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Привіт 😗
Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋')

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def handle_about_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        '👨‍🏫 Мій творець — @nikita_onoff
'
        'Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
'
        '(Хоча якщо чесно — це він мене попросив так написати 😅)

'
        '💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

'
        '🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com) 🫶',
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
