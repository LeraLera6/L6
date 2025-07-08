from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta
import asyncio
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

# --- Кнопки ---
menu_kb = InlineKeyboardMarkup(row_width=1)
menu_kb.add(
    InlineKeyboardButton("💋Про мене", callback_data="about"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
    InlineKeyboardButton("👩‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💕 Подружки для спілкування", callback_data="models")
)

# --- Групове повідомлення з кнопками ---
group_kb = InlineKeyboardMarkup(row_width=1)
group_kb.add(
    InlineKeyboardButton("💕 Подружки для спілкування", callback_data="models_chat"),
    InlineKeyboardButton("❓Задай мені питання ↗️", url="https://t.me/LERA_V6_bot?start=from_group")
)

# --- Стани автопостингу ---
last_group_post = None

# --- Старт ---
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт 😘\nЯ — Лера. Рада тебе бачити тут.\nНатисни одну з кнопок нижче, щоб дізнатись більше про мене 😛",
            reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == "about")
async def about_me(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Мені 22, я з Одеси.\nВивчала психологію і трохи магію спокуси 🥵\nЛюблю бути загадкою у чаті...",
        reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == "goal")
async def project_goal(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 😛\n\n💬 І пам’ятай — усе це є частиною проєкту <a href='https://t.me/+d-pPVpIW-UBkZGUy'>brEAst</a> — нашого особливого Telegram-чату спокуси та фантазій.",
        reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == "creator")
async def about_creator(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👩‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки <a href='https://openai.com'>OpenAI</a>. Дякую їм за це 🤝",
        reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == "models")
async def models(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "💕 Подружки для спілкування\nЯкщо хочеш приємно провести час онлайн — напиши одній з моїх подруг 😊\nОсь вони: https://t.me/virt_chat_ua1/134421",
        reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == "models_chat")
async def models_group(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply(
        "💕 Подружки для спілкування\nЯкщо хочеш приємно провести час онлайн — напиши одній з моїх подруг 😊\nОсь вони: https://t.me/virt_chat_ua1/134421")

# --- Автопостинг у групі ---
async def group_autopost():
    global last_group_post
    while True:
        try:
            if datetime.utcnow().minute % 30 == 0:
                now = datetime.utcnow()
                if not last_group_post or (now - last_group_post) >= timedelta(minutes=30):
                    await bot.send_message(GROUP_CHAT_ID,
                        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг. Чи Задай мені питання", 
                        reply_markup=group_kb)
                    last_group_post = now
            await asyncio.sleep(60)
        except Exception as e:
            logging.exception(e)
            await asyncio.sleep(60)

# --- Стартер ---
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(group_autopost())
    executor.start_polling(dp, skip_updates=True)
