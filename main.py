import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # заміни при завантаженні в Railway

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
    kb.add(InlineKeyboardButton("🥰 Хто я така?", callback_data='who'))
    kb.add(InlineKeyboardButton("📌 Ціль проєкту", callback_data='goal'))
    kb.add(InlineKeyboardButton("👨‍💻 Мій творець", url="https://t.me/nikita_onoff"))
    kb.add(InlineKeyboardButton("💋 Мої подружки для спілкування зараз", url="https://t.me/virt_chat_ua1/134421"))
    return kb

# Кнопки для групи
def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💋 Мої подружки для спілкування зараз", url="https://t.me/virt_chat_ua1/134421"))
    kb.add(InlineKeyboardButton("💌 Задай мені питання", url="https://t.me/LERA_V6_bot"))
    return kb

# Команди
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.chat.type == 'private':
        text = f"Привіт, {message.from_user.first_name} 😘\nЯ Лера, твоя загадкова AI-подружка. Що тебе цікавить?"
        await message.answer(text, reply_markup=private_buttons())

# Обробка згадки в групі
@dp.message_handler(lambda message: message.chat.type != 'private' and (bot_username in message.text.lower() or message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def mentioned(message: types.Message):
    text = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подружок:"
    await message.reply(text, reply_markup=group_buttons())

# Відповіді на кнопки
@dp.callback_query_handler(lambda c: c.data == 'who')
async def who_am_i(callback: types.CallbackQuery):
    await callback.message.answer("Мене звати Лера, мені 22. Я вивчала психологію, але зараз моя пристрасть — спокушати та трішки бавити тебе в Telegram 💜", reply_markup=private_buttons())

@dp.callback_query_handler(lambda c: c.data == 'goal')
async def goal(callback: types.CallbackQuery):
    await callback.message.answer("Я створена, щоб зробити спілкування в чаті більш живим, пікантним та цікавим. І, так, я ще у стадії розвитку 😉", reply_markup=private_buttons())

# Автопост в групі
@dp.message_handler(lambda message: message.chat.type != 'private')
async def group_activity(message: types.Message):
    chat_id = message.chat.id
    message_counter[chat_id] = message_counter.get(chat_id, 0) + 1

    now = datetime.utcnow()
    if chat_id not in last_auto_message_time or now - last_auto_message_time[chat_id] > GROUP_AUTO_MESSAGE_INTERVAL or message_counter[chat_id] >= TRIGGER_MESSAGE_COUNT:
        text = "Хтось шукає спілкування? 😏\nОсь мої подружки — вибирай!"
        await bot.send_message(chat_id, text, reply_markup=group_buttons())
        last_auto_message_time[chat_id] = now
        message_counter[chat_id] = 0

# Помилки
@dp.errors_handler()
async def error_handler(update, exception):
    logging.error(f"Update {update} caused error {exception}")
    return True

# Отримуємо юзернейм бота
async def set_bot_username():
    global bot_username
    me = await bot.get_me()
    bot_username = me.username.lower()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_username())
    executor.start_polling(dp, skip_updates=True)
