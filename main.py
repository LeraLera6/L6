from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

ABOUT_TEXT = "👥 Я Лера — AI-дівчина из Одессы, мне 22 🖤"
PROJECT_GOAL = "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦"
CREATOR_INFO = "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶."
MODELS_LINK = "[https://t.me/virt_chat_ua1/134421](https://t.me/virt_chat_ua1/134421)"

kb_main = InlineKeyboardMarkup(row_width=2)
kb_main.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
    InlineKeyboardButton("👨‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=kb_main)

@dp.callback_query_handler(lambda c: c.data in ['about', 'goal', 'creator', 'models'])
async def button_handler(callback_query: types.CallbackQuery):
    text_map = {
        "about": ABOUT_TEXT,
        "goal": PROJECT_GOAL,
        "creator": CREATOR_INFO,
        "models": f"💞 Обери одну з моїх подруг тут: {MODELS_LINK}"
    }
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text_map[callback_query.data],
        reply_markup=kb_main,
        parse_mode="Markdown"
    )
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
