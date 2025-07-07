import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import datetime
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Час останнього автопосту та кількість повідомлень
last_auto_post_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
message_counter = 0

# Клавіатура для групового чату
group_keyboard = InlineKeyboardMarkup(row_width=1)
group_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="group_girls"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/LERA_V6_bot")
)

# Клавіатура для приватного чату
private_keyboard = InlineKeyboardMarkup(row_width=1)
private_keyboard.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="private_girls")
)

# Повідомлення, що надсилається при згадці або автопостингу
mention_text = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."

# Обробка callback кнопок
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "group_girls":
        await bot.send_message(
            callback_query.message.chat.id,
            "Ось мої подружки для спілкування 😘 Обери собі за посиланням: https://t.me/virt_chat_ua1/134421"
        )
    elif data == "private_girls":
        await bot.send_message(
            callback_query.from_user.id,
            "Ось мої подружки для спілкування 😘 Обери собі за посиланням: https://t.me/virt_chat_ua1/134421"
        )
    elif data == "about_me":
        await bot.send_message(callback_query.from_user.id, "👥 Я — Лера. Та, що поруч, навіть якщо ми ще не знайомі.\n\nМоже, я всього лише бот... Але я створена, щоб бути трохи більшою, ніж просто кодом 💋")
    elif data == "project_goal":
        await bot.send_message(callback_query.from_user.id, "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 💋\n\n🗯 І памʼятай — усе це є частиною проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy) — нашого особливого Telegram-чату спокуси та фантазій.", parse_mode="Markdown")
    elif data == "creator":
        await bot.send_message(callback_query.from_user.id, "👨‍🏫 Мій творець — @nikita_onoff.\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)")

# Обробка згадок у групі
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"] and "@LERA_V6_bot" in message.text)
async def handle_mention(message: types.Message):
    global last_auto_post_time, message_counter

    last_auto_post_time = datetime.datetime.now()
    message_counter = 0

    await bot.send_message(message.chat.id, mention_text, reply_markup=group_keyboard)

# Автоматичний постинг кожні 30 хв або після 5 повідомлень
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"])
async def track_activity(message: types.Message):
    global last_auto_post_time, message_counter

    message_counter += 1
    now = datetime.datetime.now()
    if (now - last_auto_post_time).total_seconds() >= 1800 or message_counter >= 5:
        last_auto_post_time = now
        message_counter = 0
        await bot.send_message(message.chat.id, mention_text, reply_markup=group_keyboard)

# Обробка старту в ЛС
@dp.message_handler(commands=["start"])
async def start_private(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Привіт... Мені приємно, що ти мені написав 💋\nЧого б ти хотів?.. Або обери одну з опцій нижче ⬇️", reply_markup=private_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
