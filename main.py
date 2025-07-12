import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import datetime

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# === Кнопки для личных сообщений ===
def get_private_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
        InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
        InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
        InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
    )
    return keyboard

# === Ответы на кнопки ===
@dp.callback_query_handler(lambda c: c.data == 'about_me')
async def about_me_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Привіт, я Лера. Мені 22, я з Одеси. Психологиня за освітою, фліртує і трохи грається 😉\n"
        "Я не бот у прямому сенсі, я експериментальний АІ, створений для атмосфери спокуси й тепла."
    )

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def project_goal_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦"
    )

@dp.callback_query_handler(lambda c: c.data == 'creator')
async def creator_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "👨‍🏫 Мій творець — <a href='https://t.me/nikita_onoff'>@nikita_onoff</a>.\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
        "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶."
    )

@dp.callback_query_handler(lambda c: c.data == 'models')
async def models_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "💞 Обери одну з моїх подруг для особливого спілкування: <a href='https://t.me/virt_chat_ua1/134421'>дивитись список</a>"
    )

# === Хендлер для /start в особистих повідомленнях ===
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(
            "Привіт, я Лера 😇\nЯ тут, щоб зробити цей вечір трохи теплішим...\nНатискай на кнопки нижче, якщо хочеш ближче познайомитись:",
            reply_markup=get_private_keyboard()
        )

# === Автопостинг у групах ===
POST_INTERVAL_MINUTES = 30
last_post_time = {}

@dp.message_handler()
async def group_post_handler(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        global last_post_time
        now = datetime.datetime.utcnow()

        if message.chat.id not in last_post_time:
            last_post_time[message.chat.id] = now
            return

        delta = now - last_post_time[message.chat.id]
        if delta.total_seconds() >= POST_INTERVAL_MINUTES * 60:
            await message.answer(
                "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
                    InlineKeyboardButton("❓ Задай мені питання ↗️", url=f"https://t.me/{(await bot.me()).username}")
                )
            )
            last_post_time[message.chat.id] = now

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
