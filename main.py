import logging
from aiogram import Bot, Dispatcher, types, executor
import openai
import asyncio
import os

# Логи
logging.basicConfig(level=logging.INFO)

# Переменные среды
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("GPT_ID")

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# ============================== GPT Assistant ==============================

async def ask_openai_assistant(message_text, thread_id=None):
    try:
        # Создание потока, если его нет
        if not thread_id:
            thread = openai.beta.threads.create()
            thread_id = thread.id

        # Добавление сообщения от юзера
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_text
        )

        # Запуск ассистента
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=OPENAI_ASSISTANT_ID,
        )

        # Ожидание завершения
        while True:
            status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if status.status == "completed":
                break
            await asyncio.sleep(1)

        # Получение відповіді
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        reply = messages.data[0].content[0].text.value
        return reply

    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return "Щось пішло не так… 🥺 Спробуй трохи пізніше"

# ============================== ЛС ==============================

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💞 Подружки для спілкування")
    keyboard.add("🔞 Заглянь у чат 18+")
    keyboard.add("💬 Задай мені питання")
    keyboard.add("🧑‍🏫 Про творця")
    keyboard.add("🧠 Що я вмію")
    await message.reply(
        "Привіт, я Лера 💋 Обери, що тебе цікавить 👇",
        reply_markup=keyboard,
    )

@dp.message_handler(lambda message: message.text == "💞 Подружки для спілкування")
async def send_models(message: types.Message):
    await message.reply(
        "У мене є подруги, які готові на більше…
💋 Обери свою за настроєм — ось наш список:
👉 https://t.me/virt_chat_ua1/134421"
    )

@dp.message_handler(lambda message: message.text == "🔞 Заглянь у чат 18+")
async def send_chat_link(message: types.Message):
    await message.reply(
        "Там усе трохи інакше…
🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈
👉 https://t.me/+d-pPVpIW-UBkZGUy"
    )

@dp.message_handler(lambda message: message.text == "💬 Задай мені питання")
async def start_chat(message: types.Message):
    await message.reply("Пиши мені будь-що — я відповім як твоя AI-подруга 💋")

@dp.message_handler(lambda message: message.text == "🧑‍🏫 Про творця")
async def about_creator(message: types.Message):
    await message.reply(
        "👨‍🏫 Мій творець — @nikita_onoff
"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)

"
        "💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

"
        "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
    )

@dp.message_handler(lambda message: message.text == "🧠 Що я вмію")
async def about_skills(message: types.Message):
    await message.reply(
        "Я вмію:
"
        "— відповідати на складні питання
"
        "— допомагати з текстами, думками, ідеями
"
        "— фліртувати ніжно або з вогником 😉
"
        "— і ще багато чого — просто напиши 💬"
    )

@dp.message_handler()
async def gpt_reply(message: types.Message):
    reply = await ask_openai_assistant(message.text)
    await message.reply(reply)

# ============================== Старт ==============================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
