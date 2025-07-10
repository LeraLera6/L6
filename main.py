import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from datetime import datetime, timedelta
import os

# Инициализация
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Переменные состояния
last_auto_post = datetime.now() - timedelta(minutes=31)
message_count = 0

# Кнопки в ЛС
def get_private_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
        InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
    )
    return keyboard

# Кнопки в групі
def get_group_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
        InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
    )
    return keyboard

# Автопостинг
async def auto_posting():
    global last_auto_post, message_count
    while True:
        now = datetime.now()
        if now - last_auto_post >= timedelta(minutes=30) or message_count >= 5:
            try:
                await bot.send_message(
                    chat_id=os.getenv("GROUP_ID"),
                    text="Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                    reply_markup=get_group_keyboard()
                )
                last_auto_post = now
                message_count = 0
            except Exception as e:
                logging.error(f"Ошибка автопостинга: {e}")
        await asyncio.sleep(60)

# Команда /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт, я Лера 💋 Можеш дізнатись про мене більше або обрати подружку 😘",
            reply_markup=get_private_keyboard()
        )

# Колбек кнопок
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "about_me":
        await callback_query.message.edit_text(
            "Мене звати Лера 💕\nМені 22, я з Одеси 🏖️\nЛюблю флірт, психологію та атмосферні розмови 😘"
        )
    elif data == "goal":
        await callback_query.message.edit_text(
            "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦"
        )
    elif data == "creator":
        await callback_query.message.edit_text(
            "👨‍🏫 Мій творець — [@nikita_onoff](https://t.me/nikita_onoff).\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶.\n\n📲 І все це — для Telegram-чату [brEAst](https://t.me/+d-pPVpIW-UBkZGUy)",
            disable_web_page_preview=True
        )
    elif data == "models":
        await callback_query.message.edit_text(
            "Ось мої найкращі подружки — з ними точно не засумуєш 😈\n\nОбирай: https://t.me/virt_chat_ua1/134421"
        )

# Поведінка в групах
@dp.message_handler()
async def group_handler(message: types.Message):
    global message_count, last_auto_post

    if message.chat.type in ["group", "supergroup"]:
        message_count += 1

        # Реакція на згадку @юзернейма
        if f"@{(await bot.get_me()).username.lower()}" in message.text.lower():
            await message.reply(
                "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                reply_markup=get_group_keyboard()
            )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_posting())
    executor.start_polling(dp, skip_updates=True)
