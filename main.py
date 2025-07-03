import logging
import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
menu_buttons = InlineKeyboardMarkup(row_width=1)
menu_buttons.add(
    InlineKeyboardButton("💞 Мої подружки, які хочуть з тобою поспілкуватись", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("👨‍💻 Розробник", callback_data="dev")
)

# Відповіді на повтори
repeat_responses = [
    "Мені здається, я вже відповідала 😌",
    "Я трохи втомилась, але я все ще тут…",
    "Може, спробуємо щось нове?..",
    "Я не готова зараз повторюватися… ",
    "Здається, ми вже це проходили 😉"
]

# Вітання при першому повідомленні в ЛС
def get_private_intro():
    return (
        "Привіт, я Лера 😘 Мені приємно, що ти мені написав. Як справи? Чого б ти хотів?..\n\n"
        "До речі, ось мої подружки, які дуже хочуть з тобою поспілкуватися — не соромся 😉"
    )

# Автовідповідь у групі
def get_group_intro():
    return (
        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг 💋"
    )

# Повідомлення якщо немає що сказати
def no_reply_message():
    return (
        "Ммм… я б щось сказала, але не хочу повторюватись 😇\n"
        "Можемо перейти до більш гарячих речей… обирай нижче 👇"
    )

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(get_private_intro(), reply_markup=menu_buttons)
    else:
        await message.reply("Я працюю тільки в ЛС 😉 Напиши мені приватно")

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.type != "private":
        if (message.reply_to_message and message.reply_to_message.from_user.username == bot.username) or \
           (f"@{bot.username}" in message.text):
            text = message.text.lower()
            if any(phrase in text for phrase in ["привіт", "хто тут", "не спить", "вільний"]):
                await message.reply(get_group_intro(), reply_markup=menu_buttons)
            else:
                await message.reply(no_reply_message(), reply_markup=menu_buttons)
    else:
        if hasattr(message, 'last_text') and message.text == message.last_text:
            await message.answer(random.choice(repeat_responses), reply_markup=menu_buttons)
        else:
            message.last_text = message.text
            await message.answer(get_private_intro(), reply_markup=menu_buttons)

@dp.callback_query_handler(lambda c: c.data == 'dev')
async def process_callback_dev(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Розробник бота — @nikita_onoff", reply_markup=menu_buttons)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
