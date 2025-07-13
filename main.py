import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import CommandStart
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Кнопки ---
def get_main_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="👥 Про мене", callback_data="about"),
        InlineKeyboardButton(text="🧠 Ціль проєкту", callback_data="goal"),
        InlineKeyboardButton(text="🧑‍🏫 Про мого творця", callback_data="creator"),
        InlineKeyboardButton(text="💖 Подружки для спілкування", callback_data="models")
    )
    return keyboard

# --- Автовідповідь на згадку в групі ---
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"] and (message.reply_to_message and message.reply_to_message.from_user.username == bot.username or f"@{bot.username}" in message.text))
async def mention_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="💖 Подружки для спілкування", callback_data="models"),
        InlineKeyboardButton(text="❓ Задай мені питання ↗️", url=f"https://t.me/{bot.username}")
    )
    await message.reply(
        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
        reply_markup=keyboard
    )

# --- Автопостинг у групі ---
async def auto_post():
    await bot.wait_until_ready()
    while True:
        await asyncio.sleep(1800)  # кожні 30 хв
        for dialog in await bot.get_updates():
            if dialog.message and dialog.message.chat.type in ["group", "supergroup"]:
                try:
                    keyboard = InlineKeyboardMarkup(row_width=1)
                    keyboard.add(
                        InlineKeyboardButton(text="💖 Подружки для спілкування", callback_data="models"),
                        InlineKeyboardButton(text="❓ Задай мені питання ↗️", url=f"https://t.me/{bot.username}")
                    )
                    await bot.send_message(
                        dialog.message.chat.id,
                        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                        reply_markup=keyboard
                    )
                except Exception:
                    continue

# --- Обробка команд у ЛС ---
@dp.message_handler(CommandStart(), lambda message: message.chat.type == "private")
async def send_welcome(message: types.Message):
    await message.answer(
        "Привіт, я Лера. Доволі звичайна, але той самий собі вечірній звіт 😊",
        reply_markup=get_main_buttons()
    )

@dp.callback_query_handler(lambda c: c.data == 'about')
async def about_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Я Лера. Мені 22 роки, з Одеси. Я тут, щоб дарувати тобі флірт, тепло та емоції.")

@dp.callback_query_handler(lambda c: c.data == 'goal')
async def goal_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — загляй до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🪶")

@dp.callback_query_handler(lambda c: c.data == 'creator')
async def creator_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🧶.")

@dp.callback_query_handler(lambda c: c.data == 'models')
async def models_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "👇 Обери для себе когось особливого... \n\n🔗 Список моїх подруг: https://t.me/virt_chat_ua1/134421")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_post())
    executor.start_polling(dp, skip_updates=True)
