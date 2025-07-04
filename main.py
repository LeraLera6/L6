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
    kb.add(InlineKeyboardButton("ℹ️ Про мене", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"))
    kb.add(InlineKeyboardButton("🛡️ Про мого творця", callback_data="about_creator"))
    kb.add(InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"))
    return kb

# Кнопки для групи
def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💞 Подружки для спілкування", callback_data="recommend_models"))
    kb.add(InlineKeyboardButton("❓Задай мені питання", url="https://t.me/LERA_V6_bot"))
    return kb

# Callback-обробники
@dp.callback_query_handler(lambda c: c.data == 'about_lera')
async def process_about_lera(callback_query: types.CallbackQuery):
    text = "Мені 22, я з Одеси. Вивчала психологію і трохи магію спокуси 😉\nЛюблю бути загадкою у чаті, а в особистих можу стати тією, яку ти шукав..."
    await bot.send_message(callback_query.from_user.id, text, reply_markup=private_buttons())

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def process_project_goal(callback_query: types.CallbackQuery):
    text = "Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу."
    await bot.send_message(callback_query.from_user.id, text, reply_markup=private_buttons())

@dp.callback_query_handler(lambda c: c.data == 'about_creator')
async def process_about_creator(callback_query: types.CallbackQuery):
    text = "Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉"
    await bot.send_message(callback_query.from_user.id, text, reply_markup=private_buttons())

@dp.callback_query_handler(lambda c: c.data == 'recommend_models')
async def process_models(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Ось список моїх подруг, яких я раджу: https://t.me/virt_chat_ua1/134421")

# Відповідь на згадку у групі
@dp.message_handler(lambda message: message.chat.type in ['group', 'supergroup'] and '@LERA_V6_bot' in message.text)
async def mention_response(message: types.Message):
    await message.reply("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=group_buttons())

# Автоповідомлення в групі
async def auto_posting():
    while True:
        now = datetime.utcnow()
        for chat_id, last_time in last_auto_message_time.items():
            if now - last_time >= GROUP_AUTO_MESSAGE_INTERVAL:
                await bot.send_message(chat_id, "Я поруч 😘 Пам’ятай, що мої подружки чекають на тебе тут: https://t.me/virt_chat_ua1/134421")
                last_auto_message_time[chat_id] = now
        await asyncio.sleep(60)

@dp.message_handler(lambda message: message.chat.type in ['group', 'supergroup'])
async def count_group_messages(message: types.Message):
    chat_id = message.chat.id
    message_counter[chat_id] = message_counter.get(chat_id, 0) + 1
    if message_counter[chat_id] >= TRIGGER_MESSAGE_COUNT:
        now = datetime.utcnow()
        last_time = last_auto_message_time.get(chat_id, datetime.min)
        if now - last_time >= GROUP_AUTO_MESSAGE_INTERVAL:
            await bot.send_message(chat_id, "Нагадую, що мої подружки завжди поруч 😉 https://t.me/virt_chat_ua1/134421")
            last_auto_message_time[chat_id] = now
            message_counter[chat_id] = 0

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Привіт! Я Лера. Обери, що тобі цікаво:", reply_markup=private_buttons())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_posting())
    executor.start_polling(dp, skip_updates=True)
