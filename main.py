import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from openai import OpenAI

# Telegram bot initialization
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# OpenAI initialization (v1.0.0+)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants
CHAT_LINK = "https://t.me/+d-pPVpIW-UBkZGUy"
MODELS_LINK = "https://t.me/virt_chat_ua1/134421"
OPENAI_LINK = "https://openai.com"

# Main menu
main_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💕 Подружки для спілкування", callback_data="girls"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask"),
    InlineKeyboardButton("👨‍🏫 Про творця", callback_data="creator")
)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Привіт 😊\nЯ Лера — твоя AI-подруга. Обирай, що цікавить е:",
        reply_markup=main_menu
    )

@dp.callback_query_handler(lambda c: True)
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data

    if data == "girls":
        await callback.message.answer(
            "У мене є подруги, які готові на більше...\n💋 Обери свою за настроєм — ось наш список:\n👉 " + MODELS_LINK
        )
    elif data == "chat":
        await callback.message.answer(
            "Там усе трохи інакше...\n🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n👉 " + CHAT_LINK
        )
    elif data == "creator":
        await callback.message.answer(
            "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🤝\n⬇️ " + OPENAI_LINK
        )
    elif data == "ask":
        await callback.message.answer("🤔 Напиши мені будь-що — я відповім як твоя AI-подруга 💋")

@dp.message_handler()
async def handle_message(message: types.Message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    await message.reply(response.choices[0].message.content)

if __name__ == "__main__":
    executor.start_polling(dp)
