import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
from datetime import datetime, timedelta

API_TOKEN = "YOUR_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

last_messages = {}  # chat_id: (datetime, message_count)

# --- КНОПКИ ---
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
        InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="about_creator"),
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")
    )
    return keyboard

# --- ХЕНДЛЕРИ ---
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Привіт 🌸 Я Лера. Готова до флірту?", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data == "about_me")
async def about_me(callback_query: types.CallbackQuery):
    await callback_query.message.answer("👥 Я — Лера. AI-дівчина, яка вміє слухати, інтригувати і трохи більше... 😉")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == "project_goal")
async def project_goal(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦\n\n"
        "💬 До речі, весь проєкт крутиться навколо чату [brEAst](https://t.me/+d-pPVpIW-UBkZGUy) — не прогав 😉",
        parse_mode="Markdown")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def about_creator(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "👨‍🏫 Мій творець — @nikita_onoff.\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == "girls")
async def girls(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "💞 Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг: [Список моделей](https://t.me/virt_chat_ua1/134421)",
        parse_mode="Markdown")
    await callback_query.answer()

# --- АВТО-ПОСТИНГ У ГРУПАХ ---
@dp.message_handler()
async def handle_group_activity(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        now = datetime.utcnow()
        chat_id = message.chat.id

        if chat_id not in last_messages:
            last_messages[chat_id] = (now, 1)
            return

        last_time, count = last_messages[chat_id]

        if now - last_time > timedelta(minutes=30) or count >= 5:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls"),
                InlineKeyboardButton("❓ Задай мені питання ↗️", url=f"https://t.me/{(await bot.get_me()).username}")
            )
            await message.answer("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=keyboard)
            last_messages[chat_id] = (now, 0)
        else:
            last_messages[chat_id] = (last_time, count + 1)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
