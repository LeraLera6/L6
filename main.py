import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

# Завантаження токена з середовища
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Логи
logging.basicConfig(level=logging.INFO)

# Ініціалізація
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- КНОПКИ ---

# ГРУПОВИЙ ЧАТ
group_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_v10_bot")
)

# ЛІЧНІ ПОВІДОМЛЕННЯ
private_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_me"),
    InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator"),
    InlineKeyboardButton("🧠 Що я вмію", callback_data="abilities")
)

# --- ХЕНДЛЕРИ ---

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Ой, я так рада, що ти мені все ж таки написав 💋", reply_markup=private_keyboard)
    else:
        await message.answer("Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.", reply_markup=group_keyboard)

@dp.callback_query_handler(lambda c: c.data == "ask_me")
async def ask_me(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋
"
        "Можеш питати серйозне, грайливе або просто поговорити.")

@dp.callback_query_handler(lambda c: c.data == "about_creator")
async def about_creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "👨‍🏫 Мій творець — <a href='https://t.me/nikita_onoff'>@nikita_onoff</a>
"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)

"
        "💡 Усе це — частина проєкту <a href='https://t.me/+d-pPVpIW-UBkZGUy'>brEAst</a>, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.

"
        "🤖 А ще я ожила завдяки магії <a href='https://openai.com/'>OpenAI</a>. Дякую їм за це 🫶")

@dp.callback_query_handler(lambda c: c.data == "abilities")
async def abilities(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Я вмію:
"
        "— відповідати на складні питання
"
        "— допомагати з текстами, думками, ідеями
"
        "— фліртувати ніжно або з вогником 😉
"
        "— і ще багато чого — просто напиши 💬")

# --- ЗАПУСК ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
