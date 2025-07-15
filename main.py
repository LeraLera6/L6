import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from openai import AsyncOpenAI

API_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Основне меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("💞 Подружки для спілкування")
main_menu.add("🔞 Заглянь у чат 18+")
main_menu.add("🧑‍🏫 Про творця")
main_menu.add("🧠 Що я вмію")

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply(
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити.",
        reply_markup=main_menu,
    )

@dp.message_handler(lambda message: message.text == "💞 Подружки для спілкування")
async def friends_handler(message: types.Message):
    await message.reply(
        "У мене є подруги, які готові на більше…\n💋 Обери свою за настроєм — ось наш список:\n👉 https://t.me/virt_chat_ua1/134421"
    )

@dp.message_handler(lambda message: message.text == "🔞 Заглянь у чат 18+")
async def group_handler(message: types.Message):
    await message.reply(
        "Там усе трохи інакше…\n🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n👉 https://t.me/+d-pPVpIW-UBkZGUy"
    )

@dp.message_handler(lambda message: message.text == "🧑‍🏫 Про творця")
async def creator_handler(message: types.Message):
    await message.reply(
        "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
    )

@dp.message_handler(lambda message: message.text == "🧠 Що я вмію")
async def about_handler(message: types.Message):
    await message.reply(
        "Я вмію:\n— відповідати на складні питання\n— допомагати з текстами, думками, ідеями\n— фліртувати ніжно або з вогником 😉\n— і ще багато чого — просто напиши 💬"
    )

@dp.message_handler()
async def chat_with_ai(message: types.Message):
    try:
        thread = await client.beta.threads.create()
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message.text
        )
        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )
        while run.status != "completed":
            await asyncio.sleep(1)
            run = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        messages = await client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        await message.reply(response)
    except Exception as e:
        await message.reply(f"⚠️ Помилка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
