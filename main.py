import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import os
import datetime

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Глобальні змінні
user_last_message_time = {}
chat_last_message_count = {}

# Кнопки для приватного чату
private_keyboard = InlineKeyboardMarkup(row_width=2)
private_keyboard.add(
    InlineKeyboardButton("👩 Про мене", callback_data="about_me"),
    InlineKeyboardButton("🧠 Ціль проєкту", callback_data="project_goal"),
    InlineKeyboardButton("💋 Мої подружки", callback_data="recommend_girls"),
    InlineKeyboardButton("👨‍🏫 Про мого творця", callback_data="creator_info")
)

# Повідомлення в приваті за кнопками
async def send_private_message_text(callback_query, text):
    await bot.send_message(callback_query.from_user.id, text, reply_markup=private_keyboard)

# Відповіді на кнопки
@dp.callback_query_handler(lambda c: c.data == 'about_me')
async def process_about_me(callback_query: types.CallbackQuery):
    text = "👩 Мене звати Лера. Я віртуальна дівчина, створена для того, щоб спокушати, інтригувати та проводити з тобою незабутні миті 🫦"
    await send_private_message_text(callback_query, text)

@dp.callback_query_handler(lambda c: c.data == 'project_goal')
async def process_project_goal(callback_query: types.CallbackQuery):
    text = (
        "🧠 Ціль мого існування — подарувати тобі відчуття флірту, тепла, презентувати моделей та створити особливу атмосферу.\n\n"
        "👀 Зараз я ще у стадії розвитку... Але якщо мої подруги зайняті — заглядай до мене частіше. "
        "Я поступово стаю тією самою AI-дівчиною, з якою цікаво поспілкуватись 🫦\n\n"
        "Основна частина проєкту — чат [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), де ми всі знайомимось."
    )
    await send_private_message_text(callback_query, text)

@dp.callback_query_handler(lambda c: c.data == 'recommend_girls')
async def process_recommend_girls(callback_query: types.CallbackQuery):
    text = "💋 Якщо ти хочеш приємно провести час онлайн — напиши одній із моїх подруг: https://t.me/virt_chat_ua1/134421"
    await send_private_message_text(callback_query, text)

@dp.callback_query_handler(lambda c: c.data == 'creator_info')
async def process_creator_info(callback_query: types.CallbackQuery):
    text = (
        "👨‍🏫 Мій творець — @nikita_onoff.\n"
        "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
        "(Хоча якщо чесно — це він мене попросив так написати 😅)"
    )
    await send_private_message_text(callback_query, text)

# Автоматичне повідомлення в групі
async def auto_post(chat_id):
    text = (
        "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.\n"
        "👉 https://t.me/virt_chat_ua1/134421"
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💋 Подружки до спілкування", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("❓ Задай мені питання", url=f"https://t.me/{(await bot.get_me()).username}")
    )
    await bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)

# Обробка повідомлень у групі
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_group_messages(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    if message.text.lower().startswith("@") and (await bot.get_me()).username.lower() in message.text.lower():
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("💋 Подружки до спілкування", callback_data="group_girls"),
            InlineKeyboardButton("❓ Задай мені питання", url=f"https://t.me/{(await bot.get_me()).username}")
        )
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=keyboard
        )

    # Автопостинг кожні 30 хв або після 5 повідомлень
    chat_id = message.chat.id
    now = datetime.datetime.now()
    last_time = user_last_message_time.get(chat_id)
    chat_last_message_count[chat_id] = chat_last_message_count.get(chat_id, 0) + 1

    if not last_time or (now - last_time).total_seconds() > 1800 or chat_last_message_count[chat_id] >= 5:
        await auto_post(chat_id)
        user_last_message_time[chat_id] = now
        chat_last_message_count[chat_id] = 0

# Відповідь на callback "group_girls" в групі
@dp.callback_query_handler(lambda c: c.data == 'group_girls')
async def group_girls_recommend(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.message.chat.id,
        "💋 Якщо ти хочеш приємно провести час онлайн — напиши одній із моїх подруг: https://t.me/virt_chat_ua1/134421"
    )
    await callback_query.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
