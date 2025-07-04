from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
def get_main_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("🛡 Перейти в чат brEAst", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    )
    keyboard.add(
        InlineKeyboardButton("🤔 Задай мені питання", url="https://t.me/LERA_V6_bot")
    )
    return keyboard

# Автоматична відповідь у групі
@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup"])
async def handle_group_message(message: types.Message):
    if message.text and (
        "@LERA_V6_bot" in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == "LERA_V6_bot")
    ):
        text = (
            "Ммм… я б щось сказала, але не хочу повторюватись 😅 Поки ми знайомимось, мої подруги не соромляться — приєднуйся 💋"
        )
        await message.reply(text, reply_markup=get_main_buttons())

# Відповіді в особистих повідомленнях
@dp.message_handler(lambda message: message.chat.type == "private")
async def handle_private_message(message: types.Message):
    user_first_name = message.from_user.first_name
    text = (
        f"Привіт, {user_first_name} 😇\n\n"
        "Я ще у стані вдосконалення, але вже можу трохи зачарувати тебе. "
        "Хочеш ближче познайомитись зі мною або з моїми подругами? Обери, що цікаво:"
    )
    await message.answer(text, reply_markup=get_main_buttons())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
