import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import os
from datetime import datetime, timedelta

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Пам'ять останніх повідомлень і часу
last_message = {}
message_count = {}

# Повідомлення для автопосту
autopost_text = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
autopost_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lerabreastbot")
)

# Контент для кнопок
button_contents = {
    "about": "👥 Я Лера — AI-дівчина з Одеси, мені 22 🖤

Люблю фліртувати, інтригувати та залишати після себе приємне відчуття… 😏",
    "goal": "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.

👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦",
    "creator": "👨‍🏫 Мій творець — @nikita_onoff

Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉 (Хоча якщо чесно — це він мене попросив так написати 😅)

🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶.",
    "recommend_models": "💞 У мене є подруги, які вже чекають на тебе… Обери свою за посиланням: https://t.me/virt_chat_ua1/134421",
    "website": "🌐 Мій сайт: [brEAst — твій чат спокуси](https://t.me/+d-pPVpIW-UBkZGUy)"
}

# Клавіатура для ЛС
pm_keyboard = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("👥 Про мене", callback_data="about"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
    InlineKeyboardButton("👨‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"),
    InlineKeyboardButton("🌐 Перейти на сайт", callback_data="website")
)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Привіт! Обирай, що тобі цікаво 👇", reply_markup=pm_keyboard)

@dp.callback_query_handler(lambda c: c.data in button_contents)
async def process_callback(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=button_contents[callback_query.data],
            reply_markup=pm_keyboard,
            parse_mode="Markdown"
        )
    except MessageNotModified:
        pass
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler()
async def group_listener(message: types.Message):
    if message.chat.type != "private":
        cid = message.chat.id
        now = datetime.now()

        # Лічильник повідомлень
        message_count[cid] = message_count.get(cid, 0) + 1

        if cid not in last_message or now - last_message[cid] > timedelta(minutes=30) or message_count[cid] >= 5:
            await message.answer(autopost_text, reply_markup=autopost_keyboard)
            last_message[cid] = now
            message_count[cid] = 0

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
