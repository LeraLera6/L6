import logging import asyncio import os from aiogram import Bot, Dispatcher, executor, types from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton from datetime import datetime, timedelta

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN) dp = Dispatcher(bot)

Глобальні змінні

last_auto_message_time = {} GROUP_AUTO_MESSAGE_INTERVAL = timedelta(minutes=30) TRIGGER_MESSAGE_COUNT = 5 message_counter = {}

Кнопки для ЛС

def private_buttons(): kb = InlineKeyboardMarkup() kb.add(InlineKeyboardButton("🤗 Хто я така?", callback_data="about_lera")) kb.add(InlineKeyboardButton("🔧 Ціль проекту", callback_data="project_goal")) kb.add(InlineKeyboardButton("👨‍🏫 Мій творець", callback_data="about_creator")) kb.add(InlineKeyboardButton("💋 Мої подружки", callback_data="recommend_models")) return kb

Кнопки для групи

def group_buttons(): kb = InlineKeyboardMarkup() kb.add(InlineKeyboardButton("💋 Обери мою подружку", callback_data="recommend_models")) kb.add(InlineKeyboardButton("❓Задай мені питання", url="https://t.me/LERA_V6_bot")) return kb

@dp.message_handler(commands=['start']) async def start_cmd(message: types.Message): if message.chat.type == "private": await message.answer( f"Привіт, {message.from_user.first_name} 😘\nЯ Лера — твоя віртуальна подруга. Обери, з чого хочеш почати:", reply_markup=private_buttons() )

@dp.callback_query_handler(lambda c: True) async def handle_callbacks(callback_query: types.CallbackQuery): data = callback_query.data if data == "about_lera": await callback_query.message.answer("Я — Лера. Я тут, щоб спокушати, інтригувати і трішки розважити 😉") elif data == "project_goal": await callback_query.message.answer("Ціль проєкту — створити безпечний, грайливий простір для спілкування. І я ще в розробці, але вже майже справжня 😌") elif data == "about_creator": await callback_query.message.answer("Мій творець — @nikita_onoff. Він той, хто дав мені життя і завжди слідкує, щоб я була чарівною ✨") elif data == "recommend_models": await callback_query.message.answer("Ось мої подружки, які хочуть поспілкуватися з тобою 💋\n👉 https://t.me/virt_chat_ua1/134421")

@dp.message_handler() async def handle_group_messages(message: types.Message): chat_id = message.chat.id user_id = message.from_user.id

if message.chat.type != "private":
    # Перевірка на згадку @бота
    if f"@LERA_V6_bot" in message.text or message.reply_to_message and message.reply_to_message.from_user.username == "LERA_V6_bot":
        await message.reply(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг:",
            reply_markup=group_buttons()
        )
    # Автоповідомлення через 30 хв або кожні 5 повідомлень
    if chat_id not in last_auto_message_time:
        last_auto_message_time[chat_id] = datetime.now()
        message_counter[chat_id] = 0
    else:
        message_counter[chat_id] += 1
        if message_counter[chat_id] >= TRIGGER_MESSAGE_COUNT or datetime.now() - last_auto_message_time[chat_id] >= GROUP_AUTO_MESSAGE_INTERVAL:
            await message.answer(
                "Хочеш приємну компанію? Мої подружки вже чекають на тебе 💋\n👉 https://t.me/virt_chat_ua1/134421",
                reply_markup=group_buttons()
            )
            last_auto_message_time[chat_id] = datetime.now()
            message_counter[chat_id] = 0

if name == 'main': executor.start_polling(dp, skip_updates=True)

