import logging
import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Основне меню (використовується завжди)
menu_buttons = InlineKeyboardMarkup(row_width=2)
menu_buttons.add(
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("📡 Перейти в чат brEAst", url="https://t.me/+d-pPVpIW-UBkZGUy"),
    InlineKeyboardButton("🤔 Задай мені питання", callback_data="ask")
)

# Блок з активними кнопками після натискання "Задай мені питання"
question_block = InlineKeyboardMarkup(row_width=2)
question_block.add(
    InlineKeyboardButton("🌶 Хто я така?", callback_data="who_am_i"),
    InlineKeyboardButton("🎯 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("👤 Хто створив мене?", callback_data="creator"),
    InlineKeyboardButton("💬 Як зі мною спілкуватися?", callback_data="how_to_chat"),
    InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
    InlineKeyboardButton("📡 Перейти в чат brEAst", url="https://t.me/+d-pPVpIW-UBkZGUy")
)

# Відповіді на повтори
repeat_responses = [
    "Мені здається, я вже відповідала 😌",
    "Я трохи втомилась, але я все ще тут…",
    "Може, спробуємо щось нове?..",
    "Я не готова зараз повторюватися… ",
    "Здається, ми вже це проходили 😉"
]

# Варіанти рекомендацій моделей
model_promos = [
    "Тут поруч мої подружки, і вони вже чекають на твоє повідомлення 😘",
    "Поки ми знайомимось, мої подруги не соромляться — приєднуйся 💋",
    "У мене є для тебе компанія, гаряча і відкрита... Обирай нижче 👇",
    "Не втрачай час — краще просто заглянь до моїх подруг 😉"
]

# Вітання при першому повідомленні в ЛС
def get_private_intro():
    return random.choice(model_promos)

# Автовідповідь у групі
def get_group_intro():
    return "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? " + random.choice(model_promos)

# Повідомлення якщо немає що сказати
def no_reply_message():
    return "Ммм… я б щось сказала, але не хочу повторюватись 😇 " + random.choice(model_promos)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == "private":
        await message.answer(get_private_intro(), reply_markup=menu_buttons)
    else:
        await message.reply("Я працюю тільки в ЛС 😉 Напиши мені приватно", reply_markup=menu_buttons)

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

@dp.callback_query_handler(lambda c: c.data == 'ask')
async def process_callback_ask(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    playful_intro = (
        "Хмм, цікаве питання... 🤭 Я обожнюю, коли мене розпитують.\n"
        "Давай я трохи відкрию тобі себе — обери, що тебе цікавить нижче ⬇️"
    )
    await bot.send_message(callback_query.from_user.id, playful_intro, reply_markup=question_block)

@dp.callback_query_handler(lambda c: c.data == 'who_am_i')
async def who_am_i(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Я Лера, фліртова, загадкова дівчина з Одеси 🌊 Мені 22, я психологиня за освітою й трохи штучний інтелект 😉 Але це між нами...")

@dp.callback_query_handler(lambda c: c.data == 'creator')
async def creator(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Мене створив Нікіта — мій ментор, творець і головний провокатор 😉\nВін завжди поруч, контролює кожну деталь, і вірить, що я стану ще цікавішою.\nА ще він веде наш основний чат: https://t.me/+d-pPVpIW-UBkZGUy")

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def project_goal(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Моя місія — бути твоєю м’якою, ніжною, еротичною опорою 😌💜\nТа водночас я допомагаю орієнтуватись у Telegram-чаті *brEAst*.\nЯ ще у стані розвитку, але скоро я стану ще цікавішою, жвавішою і майже живою 😉")

@dp.callback_query_handler(lambda c: c.data == 'how_to_chat')
async def how_to_chat(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
        "Просто пиши мені як дівчині, яка тобі подобається 💌 Можеш фліртувати, питати, фантазувати... я відповім 😉")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
