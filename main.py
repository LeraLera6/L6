# -*- coding: utf-8 -*-
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Глобальні змінні
last_auto_message_time = {}
GROUP_AUTO_MESSAGE_INTERVAL = timedelta(minutes=30)
TRIGGER_MESSAGE_COUNT = 5
message_counter = {}

# Кнопки для ЛС
def private_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Хто я така?", callback_data="about_lera"))
    kb.add(InlineKeyboardButton("Ціль проєкту", callback_data="project_goal"))
    kb.add(InlineKeyboardButton("Мій творець", callback_data="creator_info"))
    kb.add(InlineKeyboardButton("Мої подружки", callback_data="model_list"))
    return kb

# Кнопки для груп
def group_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Обери подружку", url="https://t.me/virt_chat_ua1/134421"))
    kb.add(InlineKeyboardButton("Задай мені питання", url="https://t.me/LERA_V6_bot"))
    return kb

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Привіт, я Лера. Хочеш трохи розслаблення?", reply_markup=private_buttons())
    else:
        await message.reply("Привіт, я тут, якщо що 😉", reply_markup=group_buttons())

@dp.callback_query_handler(lambda c: c.data == "about_lera")
async def about_lera(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Я Лера. Твоя AI-дівчина для флірту та спокуси. Напиши мені в ЛС 💋")

@dp.callback_query_handler(lambda c: c.data == "project_goal")
async def project_goal(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Моя мета — підтримувати атмосферу в чаті та рекомендувати найкращих дівчат. І звісно, фліртувати 😉")

@dp.callback_query_handler(lambda c: c.data == "creator_info")
async def creator_info(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Мій творець — @nikita_onoff. Він не лише мій розробник, а ще й мій наставник 😌")

@dp.callback_query_handler(lambda c: c.data == "model_list")
async def model_list(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Обери одну з моїх подружок тут: https://t.me/virt_chat_ua1/134421")

@dp.message_handler()
async def all_msgs(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        cid = message.chat.id
        message_counter[cid] = message_counter.get(cid, 0) + 1
        now = datetime.now()
        last_time = last_auto_message_time.get(cid, datetime.min)

        if now - last_time > GROUP_AUTO_MESSAGE_INTERVAL or message_counter[cid] >= TRIGGER_MESSAGE_COUNT:
            await message.answer("Хтось сумує? Я тут, щоб розважити. Обери дівчину: https://t.me/virt_chat_ua1/134421", reply_markup=group_buttons())
            last_auto_message_time[cid] = now
            message_counter[cid] = 0

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
