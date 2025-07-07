import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Глобальні змінні
last_auto_message_time = {}
GROUP_AUTO_MESSAGE_INTERVAL = timedelta(minutes=30)
TRIGGER_MESSAGE_COUNT = 5
message_counter = {}

# Кнопки для ЛС
def private_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👥 Про мене", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"))
    kb.add(InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="about_creator"))
    kb.add(InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"))
    return kb

# Кнопки для групи
def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"))
    kb.add(InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/LERA_V6_bot"))
    return kb

# Повідомлення автопостингу та при згадці Лери в чаті
MENTION_TEXT = """
Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.
"""

# Відповідь у ЛС при натисканні "Задай мені питання"
PRIVATE_WELCOME = """
Мені приємно, що ти мені написав 😌
Чого б ти хотів? Обери нижче 👇
"""

# Обробка згадки в групі
@dp.message_handler(lambda message: message.text and f"@{(await bot.get_me()).username}" in message.text)
async def mention_handler(message: types.Message):
    await message.reply(MENTION_TEXT, reply_markup=group_buttons())

# Обробка callback кнопок у групі
@dp.callback_query_handler(lambda c: c.data == "recommend_models")
async def recommend_models_group(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Мої подружки якраз вільні 😘 Обирай когось тут: https://t.me/virt_chat_ua1/134421")
    await call.answer()

# Обробка старту в ЛС
@dp.message_handler(commands=['start'])
async def start_private(message: types.Message):
    if message.chat.type == "private":
        await message.answer(PRIVATE_WELCOME, reply_markup=private_buttons())

# Обробка callback кнопок у ЛС
@dp.callback_query_handler(lambda c: True)
async def private_callbacks(call: types.CallbackQuery):
    if call.data == "about_lera":
        await call.message.answer("Я Лера — твоя AI-подруга, яка завжди поруч 😌 Можу підтримати розмову, підняти настрій або просто побути поруч. Звісно, якщо мої подружки з чату зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦")
    elif call.data == "project_goal":
        await call.message.answer("🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦\n\nВсе це частина великого проєкту Telegram-чату brEAst: https://t.me/+d-pPVpIW-UBkZGUy")
    elif call.data == "about_creator":
        await call.message.answer("👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)")
    elif call.data == "recommend_models":
        await call.message.answer("Якщо хочеш приємно провести час онлайн — напиши одній з моїх подружок 💕 Вони тут: https://t.me/virt_chat_ua1/134421")
    await call.answer()

# Автопостинг в чаті
@dp.message_handler(lambda message: message.chat.type != "private")
async def auto_message(message: types.Message):
    chat_id = message.chat.id
    now = datetime.now()

    message_counter[chat_id] = message_counter.get(chat_id, 0) + 1
    last_time = last_auto_message_time.get(chat_id, now - GROUP_AUTO_MESSAGE_INTERVAL)

    if now - last_time >= GROUP_AUTO_MESSAGE_INTERVAL or message_counter[chat_id] >= TRIGGER_MESSAGE_COUNT:
        await bot.send_message(chat_id, MENTION_TEXT, reply_markup=group_buttons())
        last_auto_message_time[chat_id] = now
        message_counter[chat_id] = 0

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
