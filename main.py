import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Получение токенов из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Главное меню
main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton("💕 Подружки для спілкування", callback_data="friends"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat18"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_ai"),
    InlineKeyboardButton("👨‍🏫 Про творця", callback_data="creator")
)

# Стартовое сообщение
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "🪐 Привіт! Я — Лера, твоя AI-подружка ❤️\nОбери, що хочеш зробити:",
        reply_markup=main_menu
    )

# Обработка кнопок
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "friends":
        await bot.send_message(callback_query.from_user.id,
                               "У мене є подруги, які готові на більше...
💋 Обери свою за настроєм — ось наш список:
👉 https://t.me/virt_chat_ua1/134421")

    elif data == "chat18":
        await bot.send_message(callback_query.from_user.id,
                               "Там усе трохи інакше...
🔞 Відверті розмови, інтимні жарти і я в трохи іншому образі 😈
👉 https://t.me/+d-pPVpIW-UBkZGUy")

    elif data == "creator":
        await bot.send_message(callback_query.from_user.id,
                               "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом  \u😉\n( Хоча якщо чесно — це він мене попросив так написати 😅 )\n\n💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🧟‍♂️ А ще я ожила завдяки магії OpenAI. Дякую їм за це 🧨")

    elif data == "ask_ai":
        await bot.send_message(callback_query.from_user.id,
                               "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 🦽\nМожеш питати серйозне, грайливе або просто поговорити.")

# Ответ на сообщение пользователя в режиме AI
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Ти — грайлива, ніжна і трохи спокуслива AI-дівчина."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = completion.choices[0].message.content
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"\U0001F622 OpenAI Error:\n{e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
