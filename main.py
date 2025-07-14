import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import openai
import os

# Инициализация
API_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки для ЛС
private_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_question"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")
)

# Кнопки для чата
group_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V8_bot")
)

# Автопостинг: контроль сообщений
message_count = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Привіт, я Лера. Твоя AI-подружка 💋", reply_markup=private_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def process_creator(callback_query: types.CallbackQuery):
    text = (
        "👨‍🏫 Мій творець — @nikita_onoff\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), \n"
        "створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
        "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶"
    )
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data == 'ask_question')
async def ask_question(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
        "Можеш питати серйозне, грайливе або просто поговорити."
    )

@dp.message_handler(lambda message: message.chat.type == 'private')
async def gpt_reply(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти ніжна, фліртова AI-дівчина на ім’я Лера."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"😓 OpenAI Error:\n{str(e)}")

@dp.message_handler(lambda message: message.chat.type != 'private')
async def group_monitor(message: types.Message):
    chat_id = message.chat.id
    message_count[chat_id] = message_count.get(chat_id, 0) + 1

    if message_count[chat_id] >= 5:
        await message.answer(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )
        message_count[chat_id] = 0

async def auto_posting():
    await bot.wait_until_ready()
    while True:
        for chat_id in message_count:
            try:
                await bot.send_message(
                    chat_id,
                    "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                    reply_markup=group_keyboard
                )
            except Exception as e:
                logging.warning(f"Auto-posting error: {e}")
        await asyncio.sleep(1800)  # 30 минут

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(auto_posting())
    executor.start_polling(dp, skip_updates=True)
