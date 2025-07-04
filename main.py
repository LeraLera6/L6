import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.callback_data import CallbackData

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

callback_data = CallbackData("btn", "action")

# --- КНОПКИ для ЛС ---
private_keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("ℹ️ Про мене", callback_data=callback_data.new(action="about")),
    InlineKeyboardButton("🧠 Ціль проекту", callback_data=callback_data.new(action="goal")),
    InlineKeyboardButton("🛡️ Про мого творця", callback_data=callback_data.new(action="creator")),
    InlineKeyboardButton("⬅️ Повернутись в чат", url="https://t.me/+d-pPVpIW-UBkZGUy")
)

# --- КНОПКИ для ГРУПИ ---
group_keyboard = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("🛡️ Перейти в чат brEAst", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("🤔 Задай мені питання", url="https://t.me/LERA_V6_bot")
)

# --- /start ---
@dp.message_handler(commands=["start"], chat_type=types.ChatType.PRIVATE)
async def start_private(message: types.Message):
    user_name = message.from_user.first_name
    text = f"<b>Привіт, {user_name}</b> 😇\n\nЯ ще у стані вдосконалення, але вже можу трохи зачарувати тебе.\n\nХочеш ближче познайомитись зі мною або з моїми подругами? Обери, що цікаво:"
    await message.answer(text, reply_markup=private_keyboard)

# --- Реакції на callback-кнопки в ЛС ---
@dp.callback_query_handler(callback_data.filter())
async def callback_handler(query: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "about":
        await query.message.answer("Я Собі люблю бути загадкою у чаті, але в особистих можу стати тією, яку ти хотів. 😉")
    elif action == "goal":
        await query.message.answer("Ціль моєї появи проста — подарувати відчуття флірту та теплоти, презентувати підружок та створити атмосферу.")
    elif action == "creator":
        await query.message.answer("Мій творець — нестандартний та точний. Він любить заглядати в глибину суті кожної ідеї. 😊")
    await query.answer()

# --- Реакція в групі на згадку або reply ---
@dp.message_handler(lambda message: message.chat.type != types.ChatType.PRIVATE)
async def group_react(message: types.Message):
    if f"@{bot.username}" in message.text or message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        await message.reply(
            "Ммм... я б щось сказала, але не хочу повторюватись 😁 \n\nПоки ми знайомимось, мої подруги не соромляться — приєднуйся 💋",
            reply_markup=group_keyboard
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
