import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- КНОПКИ ---
menu_buttons = InlineKeyboardMarkup(row_width=1)
menu_buttons.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="about_creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")
)

chat_buttons = InlineKeyboardMarkup(row_width=1)
chat_buttons.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/LERA_V6_bot")
)

# --- ВІДПОВІДІ НА КНОПКИ ---
@dp.callback_query_handler(lambda c: c.data == "about_me")
async def about_me(callback_query: types.CallbackQuery):
    text = ("Мені 22, я з Одеси.\n"
            "Вивчала психологію і трохи магію спокуси 😉\n"
            "Люблю бути загадкою у чаті…")
    await callback_query.message.edit_text(text, reply_markup=menu_buttons)

@dp.callback_query_handler(lambda c: c.data == "project_goal")
async def project_goal(callback_query: types.CallbackQuery):
    text = ("🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
            "👀 Зараз я ще у стадії розвитку...\n"
            "Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 💋\n\n"
            "💬 І пам’ятай — усе це є частиною проєкту brEAst — нашого особливого Telegram-чату спокуси та фантазій.")
    await callback_query.message.edit_text(text, reply_markup=menu_buttons)

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def about_creator(callback_query: types.CallbackQuery):
    text = ("👨‍🏫 Мій творець — @nikita_onoff.\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)")
    await callback_query.message.edit_text(text, reply_markup=menu_buttons)

@dp.callback_query_handler(lambda c: c.data == "girls")
async def girls(callback_query: types.CallbackQuery):
    text = ("💞 Подружки для спілкування\n"
            "Якщо хочеш приємно провести час онлайн — напиши одній з моїх подруг 😊\n"
            "Ось вони: https://t.me/virt_chat_ua1/134421")
    await callback_query.message.edit_text(text, reply_markup=menu_buttons)

# --- СТАРТ ---
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Привіт 👋 Я — Лера. Запитай мене щось або обери пункт нижче:", reply_markup=menu_buttons)

# --- АВТОПОСТИНГ У ГРУПІ ---
async def autopost():
    await bot.wait_until_ready()
    while True:
        await asyncio.sleep(1800)  # 30 хвилин
        for chat_id in active_group_chats:
            try:
                await bot.send_message(
                    chat_id,
                    "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                    reply_markup=chat_buttons
                )
            except Exception as e:
                logging.warning(f"Автопостинг помилка у чаті {chat_id}: {e}")

# Список активних груп (можна динамічно оновлювати)
active_group_chats = set()

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member_handler(message: types.Message):
    active_group_chats.add(message.chat.id)

# --- ЗАПУСК ---
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(autopost())
    executor.start_polling(dp, skip_updates=True)
