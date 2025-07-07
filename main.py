import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import Throttled

API_TOKEN = os.getenv("API_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Кнопки ---
menu_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("👥 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="goal"),
    InlineKeyboardButton("🧑‍🏫 Про мого творця", callback_data="creator"),
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
)

group_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💞 Подружки для спілкування", callback_data="models"),
    InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V6_bot")
)

# --- Команди /start ---
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(
            "Привіт, я Лера 😘\n\nОбери, що тобі цікаво:",
            reply_markup=menu_keyboard
        )

# --- Обробка натискань на кнопки ---
@dp.callback_query_handler(lambda c: c.data == "about_me")
async def about_me(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👥 Я — Лера. AI-дівчина, яка вміє фліртувати й підтримувати настрій. "
        "Ти можеш поговорити зі мною, або обрати іншу модель 😉",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "goal")
async def goal(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. "
        "Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "creator")
async def creator(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👨‍🏫 Мій творець — @nikita_onoff.\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)",
        reply_markup=menu_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "models")
async def models(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == "private":
        await callback_query.message.edit_text(
            "💞 У мене є подружки, які не менш цікаві, ніж я…\n"
            "🔗 Обери ту, яка тобі до душі: https://t.me/virt_chat_ua1/134421",
            reply_markup=menu_keyboard
        )
    else:
        await callback_query.message.answer(
            "💋 Ось список моїх подружок для спілкування: https://t.me/virt_chat_ua1/134421",
            reply_markup=group_keyboard
        )

# --- Автопостинг у групі ---
message_counter = {}

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type != "private":
        chat_id = message.chat.id
        count = message_counter.get(chat_id, 0) + 1
        message_counter[chat_id] = count

        if count >= 5:
            await bot.send_message(
                chat_id,
                "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
                reply_markup=group_keyboard
            )
            message_counter[chat_id] = 0

    # Захист від спаму
    try:
        await dp.throttle("message", rate=1)
    except Throttled:
        return

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
