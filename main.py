import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import openai
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Токен бота та ключ OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# Глобальний стан діалогу
user_gpt_active = {}

# Головне меню
def get_main_menu():
    buttons = [
        [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")],
        [InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="group")],
        [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_me")],
        [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
        [InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Старт
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_gpt_active[message.from_user.id] = False
    await message.answer(
        "Привіт! Я — Лера. Твоя AI-подруга 🤖\nОбери одну з кнопок нижче ⤵️",
        reply_markup=get_main_menu()
    )

# Обробка кнопок
@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "models":
        await bot.send_message(user_id, "У мене є подруги, які готові на більше…\n💋 Обери свою за настроєм — ось наш список:\n👉 https://t.me/virt_chat_ua1/134421")
        user_gpt_active[user_id] = False

    elif data == "group":
        await bot.send_message(user_id, "Там усе трохи інакше…\n🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n👉 https://t.me/+d-pPVpIW-UBkZGUy")
        user_gpt_active[user_id] = False

    elif data == "creator":
        await bot.send_message(user_id,
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )
        user_gpt_active[user_id] = False

    elif data == "skills":
        await bot.send_message(user_id,
            "🧠 Я вмію:\n"
            "— відповідати на складні питання\n"
            "— допомагати з текстами, думками, ідеями\n"
            "— фліртувати ніжно або з вогником 😉\n"
            "— і ще багато чого — просто напиши 💬"
        )
        user_gpt_active[user_id] = False

    elif data == "ask_me":
        await bot.send_message(user_id,
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )
        user_gpt_active[user_id] = True

    await bot.answer_callback_query(callback_query.id)

# GPT-чат
@dp.message_handler()
async def gpt_handler(message: types.Message):
    user_id = message.from_user.id
    if not user_gpt_active.get(user_id, False):
        return

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти — фліртова AI-дівчина на ім’я Лера. Відповідай ніжно, із загадковим флером."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = completion.choices[0].message["content"]
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"😥 OpenAI Error:\n{str(e)}")
        user_gpt_active[user_id] = False

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
