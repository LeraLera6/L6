# main.py
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# === Глобальні змінні ===
autopost_interval = timedelta(minutes=30)
last_autopost_time = datetime.now() - autopost_interval
last_user_messages = {}  # для підрахунку повідомлень між автопостами

group_chat_id_log = -1002138585220  # чат логів
list_link = "https://t.me/virt_chat_ua1/134421"
main_group_id = -1002094307413

# === Кнопки ЛС ===
def get_private_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("👥‍👥 Про мене", callback_data="about"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
        InlineKeyboardButton("👩‍🏫 Про мого творця", callback_data="creator"),
        InlineKeyboardButton("💕 Подружки для спілкування", callback_data="models")
    )
    return kb

# === Кнопки чату ===
def get_group_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💕 Подружки для спілкування", callback_data="models_group"),
        InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/LERA_V6_bot")
    )
    return kb

# === Хендлер старту ===
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.chat.type == "private":
        text = "Привіт — я Лера. Рада тебе бачити 😊\n\nНатисни одну з кнопок нижче, щоб дізнатися більше про мене 👇"
        await message.answer(text, reply_markup=get_private_keyboard())

# === Обробка кнопок ===
@dp.callback_query_handler()
async def callback_handler(query: types.CallbackQuery):
    if query.data == "about":
        await query.message.edit_text("Я створена для того, щоб трохи фліртувати 😉 і бути твоєю особливою AI-дівчиною.\nМожеш писати мені в будь-який час... я тут 🤪")
    elif query.data == "goal":
        await query.message.edit_text("🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🦦")
    elif query.data == "creator":
        await query.message.edit_text("👨‍🏫 Мій творець — @nikita_onoff. \nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n🤖 А ще я ожила завдяки магії <a href='https://openai.com'>OpenAI</a>. Дякую їм за це 🫶.")
    elif query.data == "models" or query.data == "models_group":
        await query.message.answer(f"💞 Подружки для спілкування\nЯкщо хочеш приємно провести час онлайн — напиши одній з моїх подруг 😉\nОсь вони: {list_link}", reply_markup=(get_private_keyboard() if query.data == "models" else None))
        await query.answer()

# === Відповідь на згадку в групі ===
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"] and ("@LERA_V6_bot" in message.text or message.reply_to_message and message.reply_to_message.from_user.username == "LERA_V6_bot"))
async def mention_response(message: types.Message):
    await message.reply(
        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг. Чи Задай мені питання",
        reply_markup=get_group_keyboard()
    )

# === Автопостинг у групі ===
async def auto_post():
    global last_autopost_time
    while True:
        now = datetime.now()
        if now - last_autopost_time > autopost_interval:
            try:
                await bot.send_message(
                    main_group_id,
                    "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг. Чи Задай мені питання",
                    reply_markup=get_group_keyboard()
                )
                last_autopost_time = now
            except Exception as e:
                logging.error(f"AutoPost Error: {e}")
        await asyncio.sleep(60)

# === Звіт у лог-канал ===
async def daily_report():
    while True:
        now = datetime.now()
        target = now.replace(hour=22, minute=30, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        await asyncio.sleep((target - datetime.now()).seconds)
        try:
            await bot.send_message(group_chat_id_log, "Щоденний звіт: бот активний і працює 💖")
        except Exception as e:
            logging.error(f"Daily Report Error: {e}")

# === Запуск ===
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_post())
    loop.create_task(daily_report())
    executor.start_polling(dp, skip_updates=True)
