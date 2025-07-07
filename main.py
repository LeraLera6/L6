import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# === Кнопки для ЛС ===
def get_private_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Про мене", callback_data="about_me")],
        [InlineKeyboardButton(text="🧠 Ціль проєкту", callback_data="project_goal")],
        [InlineKeyboardButton(text="🧑‍🏫 Про мого творця", callback_data="about_creator")],
        [InlineKeyboardButton(text="💞 Подружки для спілкування", callback_data="chat_girls")],
    ])

# === Хендлер для старту в ЛС ===
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт 😌 Я вже чекала... Можеш дізнатися про мене більше або просто поспілкуватись зі мною нижче ❤️",
            reply_markup=get_private_keyboard()
        )

# === Хендлери для callback-кнопок ===
@dp.callback_query_handler(lambda c: c.data == 'about_me')
async def about_me_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("👥 Я — Лера. Твоя віртуальна співрозмовниця, яка вміє слухати, фліртувати і трохи більше 😏")

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def project_goal_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦"
    )

@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def about_creator_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)")

@dp.callback_query_handler(lambda c: c.data == 'chat_girls')
async def chat_girls_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("💞 Обери когось із моїх подружок — і твій вечір вже не буде таким, як раніше 😉\n\nhttps://t.me/virt_chat_ua1/134421")

# === Хендлер для згадок в групі ===
@dp.message_handler()
async def mention_handler(message: types.Message):
    if message.chat.type != "private":
        me = await bot.get_me()
        if message.text and f"@{me.username}" in message.text:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💞 Подружки для спілкування", callback_data="chat_girls")],
                [InlineKeyboardButton(text="❓ Задай мені питання ↗️", url=f"https://t.me/{me.username}")]
            ])
            await message.reply("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=keyboard)

# === Автопостинг кожні 30 хв або після 5 повідомлень ===
# (Реалізацію через background task або лічильник можна додати окремо при необхідності)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
