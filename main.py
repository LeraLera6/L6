import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Токен (бере з ENV на Railway)
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Кнопки для ЛС (під вікном вводу)
private_kb = ReplyKeyboardMarkup(resize_keyboard=True)
private_kb.add(
    KeyboardButton("💞 Подружки 🔞"),
    KeyboardButton("🔞 Заглянь у чат 18+"),
    KeyboardButton("Я хочу з тобою поспілкуватися, а ти? 🫦"),
    KeyboardButton("🧑‍🏫 Про творця")
)

# Inline кнопки для групи
group_inline_kb = InlineKeyboardMarkup(row_width=2)
group_inline_kb.add(
    InlineKeyboardButton("💞 Подружки 🔞", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("Напиши мені... 🫦", url="https://t.me/Lera_Bot10")
)

# Відповідь у ЛС на кнопку з фліртом
@dp.message_handler(lambda message: message.text == "Я хочу з тобою поспілкуватися, а ти? 🫦")
async def handle_chat_start(message: types.Message):
    await message.answer("Привіт 😌")

# Відповідь на кнопку "Про творця"
@dp.message_handler(lambda message: message.text == "🧑‍🏫 Про творця")
async def handle_creator(message: types.Message):
    await message.answer(
        "🧑‍🏫 Мій творець — @nikita_onoff
"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)

"
        "💡 Усе це — частина проєкту "
        "<a href='https://t.me/+d-pPVpIW-UBkZGUy'>brEAst</a>, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

"
        "🤖 А ще я ожила завдяки магії <a href='https://openai.com'>OpenAI</a>. Дякую їм за це 🫶",
        parse_mode="HTML"
    )

# Відповідь на кнопку "💞 Подружки 🔞" або "🔞 Заглянь у чат 18+" — не потрібна, бо це просто гіперпосилання

# Автовідповідь в групі (при згадці або автопост)
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"])
async def group_reply(message: types.Message):
    if (
        message.text and (
            "@Lera_Bot10" in message.text.lower()
            or message.reply_to_message and message.reply_to_message.from_user.username == "Lera_Bot10"
            or message.text.lower() in ["привіт", "хто тут?", "є хтось?", "напишіть мені"]
        )
    ):
        await message.reply(
            "Привіт, я дуже хочу допомогти тобі знайти справжніх дівчат, які готові з тобою поспілкуватися... 🫦",
            reply_markup=group_inline_kb
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
