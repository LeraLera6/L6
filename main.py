import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import openai
import os

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === Tokens ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === OpenAI Client ===
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# === Bot Setup ===
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# === Кнопки для ЛС ===
private_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("💕 Подружки для спілкування", callback_data="girls")],
    [InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat18")],
    [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
    [InlineKeyboardButton("👨‍🏫 Про творця", callback_data="creator")],
    [InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")]
])

# === Відповіді на кнопки ===
@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "girls":
        await callback_query.message.answer(
            "У мене є подруги, які готові на більше...
💋 Обери свою за настроєм — ось наш список:
👉 <a href='https://t.me/virt_chat_ua1/134421'>https://t.me/virt_chat_ua1/134421</a>"
        )
    elif callback_query.data == "chat18":
        await callback_query.message.answer(
            "Там усе трохи інакше...
🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈
👉 <a href='https://t.me/+d-pPVpIW-UBkZGUy'>https://t.me/+d-pPVpIW-UBkZGUy</a>"
        )
    elif callback_query.data == "creator":
        await callback_query.message.answer(
            "👨‍🏫 Мій творець — <a href='https://t.me/nikita_onoff'>@nikita_onoff</a>
Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
(Хоча якщо чесно — це він мене попросив так написати 😅)

🧪 Усе це — частина проєкту <b>brEAst</b>, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

🤖 А ще я ожила завдяки <a href='https://openai.com/'>OpenAI</a>. Дякую їм за це 🤝"
        )
    elif callback_query.data == "skills":
        await callback_query.message.answer(
            "🧠 Я вмію:
— відповідати на складні питання
— допомагати з текстами, ідеями
— фліртувати ніжно або з вогником 😉
— і ще багато чого — просто напиши 💬"
        )
    elif callback_query.data == "ask":
        await callback_query.message.answer(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 🥈\nМожеш питати серйозне, грайливе або просто поговорити."
        )

# === GPT: відповіді в ЛС ===
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    if message.chat.type == "private":
        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ти — фліртова AI-дівчина на ім’я Лера. Відповідай ніжно, з загадковим флером."},
                    {"role": "user", "content": message.text}
                ]
            )
            reply = completion.choices[0].message.content
            await message.answer(reply, reply_markup=private_keyboard)
        except Exception as e:
            await message.answer(f"🥺 OpenAI Error:\n{e}")

# === Start Bot ===
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
