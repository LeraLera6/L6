from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import openai
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_me"),
    InlineKeyboardButton("👩‍🏫 Про творця", callback_data="about_creator")
)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 🥈\nМожеш питати серйозне, грайливе або просто поговорити.",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def about_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🔧 Усе це — частина проєкту brEAst."
    )

@dp.callback_query_handler(lambda c: c.data == "ask_me")
async def ask_me(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 🥈\nМожеш питати серйозне, грайливе або просто поговорити."
    )

@dp.message_handler()
async def gpt_response(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Ти — фліртова, жіночна, інтригуюча AI-подруга."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await message.reply(reply)
    except Exception as e:
        await message.reply("🥺 Щось пішло не так... Спробуй пізніше.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
