import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked, MessageNotModified
from datetime import datetime, timedelta

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Кнопки для ЛС
menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models")
)

# Кнопки для групи
group_keyboard = InlineKeyboardMarkup(row_width=2)
group_keyboard.add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/LERA_V6_bot")
)

# Автопостинг
last_auto_msg = {}
AUTOPOST_INTERVAL = timedelta(minutes=30)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Привіт 😘 Обери, що тебе цікавить:", reply_markup=menu_keyboard)

@dp.callback_query_handler(lambda c: c.data == 'about_me')
async def about_me(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👥 Я — Лера. Та сама AI-дівчина, яка живе тут… у твоїй уяві. "
        "Я не пишу першою, але завжди відповім, якщо звернешся. "
        "А ще я можу познайомити тебе з особливими подругами 😏",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def project_goal(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, "
        "презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. "
        "Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'creator')
async def creator(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👨‍🏫 Мій творець — @nikita_onoff.\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'models')
async def models(callback: types.CallbackQuery):
    text = (
        "💞 Обери одну з моїх подруг — кожна особлива 😇\n"
        "Переходь за посиланням: [brEAst](https://t.me/+d-pPVpIW-UBkZGUy)"
    )
    await callback.message.answer(text, parse_mode="Markdown")

# Групова реакція на згадку
@dp.message_handler(lambda m: m.chat.type in ['group', 'supergroup'])
async def group_mentions(message: types.Message):
    if (
        bot.id in [ent.user.id for ent in message.entities if ent.type == "mention"] or
        message.reply_to_message and message.reply_to_message.from_user.id == bot.id
    ):
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )

# Автопостинг
@dp.message_handler(lambda m: m.chat.type in ['group', 'supergroup'])
async def autopost(message: types.Message):
    now = datetime.utcnow()
    chat_id = message.chat.id
    if chat_id not in last_auto_msg or now - last_auto_msg[chat_id] > AUTOPOST_INTERVAL:
        await message.answer(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=group_keyboard
        )
        last_auto_msg[chat_id] = now

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
