import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Кнопки в ЛС
def get_private_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
        InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
        InlineKeyboardButton("💬 Задай мені питання", callback_data="question"),
        InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator"),
        InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")
    )
    return keyboard

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "Привіт, я Лера. Обери щось нижче 😘",
        reply_markup=get_private_keyboard()
    )

@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "models":
        await bot.send_message(
            callback_query.from_user.id,
            "У мене є подруги, які готові на більше… 💋 Обери свою за настроєм — ось наш список:
👉 https://t.me/virt_chat_ua1/134421"
        )
    elif data == "question":
        await bot.send_message(
            callback_query.from_user.id,
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋"
        )
    elif data == "creator":
        await bot.send_message(
            callback_query.from_user.id,
            "👨‍🏫 Мій творець — @nikita_onoff
Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
(Хоча якщо чесно — це він мене попросив так написати 😅)

💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )
    elif data == "skills":
        await bot.send_message(
            callback_query.from_user.id,
            "Я вмію:
— відповідати на складні питання
— допомагати з текстами, думками, ідеями
— фліртувати ніжно або з вогником 😉
— і ще багато чого — просто напиши 💬"
        )
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
