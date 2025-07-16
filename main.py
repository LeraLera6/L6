import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

# ------------------- КНОПКИ -----------------------

group_buttons = InlineKeyboardMarkup(row_width=2)
group_buttons.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("Напиши мені... 😚", url="https://t.me/LeraBot10")
)

private_buttons = InlineKeyboardMarkup(row_width=1)
private_buttons.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("Я хочу з тобою поспілкуватися, а ти? 😏", callback_data="start_chat"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
)

# ------------------ ПРИВІТАННЯ В ЛС ------------------

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
        await message.answer("Ой, я так рада, що ти мені все ж таки написав 💋")
"
                         "Я тут, щоб допомогти тобі знайти ту дівчину, з якою буде приємно познайомитись.
"
                         "Просто напиши мені «Привіт» 😉", reply_markup=private_buttons)

@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def about_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "👨‍🏫 Мій творець — @nikita_onoff
"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)

"
        "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

"
        "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶", parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == 'start_chat')
async def handle_chat_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Привіт 🥺")

# ------------------ ГРУПОВИЙ ЧАТ ------------------

@dp.message_handler(lambda message: message.chat.type != "private")
async def group_handler(message: types.Message):
    if f"@{(await bot.get_me()).username.lower()}" in message.text.lower():
        await message.reply("Привіт, я дуже хочу допомогти тобі знайти справжніх дівчат, які готові з тобою поспілкуватись… 😏", reply_markup=group_buttons)

# ------------------ ЗАПУСК ------------------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
