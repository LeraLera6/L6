import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
from dotenv import load_dotenv
import openai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

user_states = {}

menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_me"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити.",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "ask_me")
async def ask_me_handler(callback_query: types.CallbackQuery):
    user_states[callback_query.from_user.id] = "chat"
    await bot.send_message(
        callback_query.from_user.id,
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити."
    )

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def about_creator_handler(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "🧑‍🏫 Мій творець — @nikita_onoff\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "🔧 Усе це — частина проєкту brEAst."
    )

@dp.message_handler()
async def gpt_chat(message: types.Message):
    if user_states.get(message.from_user.id) == "chat":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": message.text}]
            )
            reply = response.choices[0].message.content.strip()
            await message.reply(reply)
        except Exception as e:
            await message.reply("😥 Щось пішло не так... Спробуй пізніше.")
    else:
        await message.reply("Натисни '💬 Задай мені питання', щоб я могла відповісти як AI 💋")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
