import logging
from aiogram import Bot, Dispatcher, executor, types
import openai
import os

TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("💞 Подружки для спілкування")
main_keyboard.add("🔞 Заглянь у чат 18+")
main_keyboard.add("💬 Задай мені питання")
main_keyboard.add("🧑‍🏫 Про творця")

# /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        "Привіт 😘 Я Лера. Пиши мені що завгодно або обери кнопку:",
        reply_markup=main_keyboard
    )

# Кнопка 1
@dp.message_handler(lambda message: message.text == "💞 Подружки для спілкування")
async def podruzhky(message: types.Message):
    await message.answer(
        "У мене є подруги, які готові на більше… 💋\n"
        "👉 https://t.me/virt_chat_ua1/134421"
    )

# Кнопка 2
@dp.message_handler(lambda message: message.text == "🔞 Заглянь у чат 18+")
async def adult_chat(message: types.Message):
    await message.answer(
        "Там усе трохи інакше…\n"
        "🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n"
        "👉 https://t.me/+d-pPVpIW-UBkZGUy"
    )

# Кнопка 3 — запуск GPT
@dp.message_handler(lambda message: message.text == "💬 Задай мені питання")
async def ask_me(message: types.Message):
    await message.answer(
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
        "Можеш питати серйозне, грайливе або просто поговорити."
    )

# Кнопка 4 — Про творця
@dp.message_handler(lambda message: message.text == "🧑‍🏫 Про творця")
async def about_creator(message: types.Message):
    await message.answer(
        "👨‍🏫 Мій творець — @nikita_onoff\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
        "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
    )

# GPT відповіді
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Ти фліртова, грайлива, мила українська AI-подруга."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response.choices[0].message.content.strip())

    except Exception as e:
        await message.answer(f"😓 OpenAI Error:\n{e}")

# Запуск
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
