import logging
import os
from datetime import datetime, timedelta
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler
)
from openai import OpenAI
import asyncio

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = (
    "👋 Я рада тебе тут бачити 💓\n\n"
    "Ти можеш написати мені прямо особисто — я вже чекаю там… 🫦\n\n"
    "Або заглянь на мій канал — там гаряче 😈"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🩷 Напиши мені особисто... 🫦", url="https://t.me/Labi_Lola")],
    [InlineKeyboardButton("🔞 Мій канал... 🫦", url="https://t.me/+rKgDRzE3wLoyYTQy")]
])

# Команда /start — особисті повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                ["🩷 Напиши мені особисто... 🫦"],
                ["🔞 Мій канал... 🫦"],
                ["👩‍🦰 Про мене... 🫦"],
                ["👨‍🏫 Про творця"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
        await update.message.reply_text(
            "Привіт, я рада, що ти мені написав. Я так цього чекала...\n\n"
            "Ти можеш перейти за кнопками нижче або просто напиши мені \"Привіт\"... 🫦",
            reply_markup=keyboard
        )

# Обробка reply-кнопок в ЛС
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "👩‍🦰 Про мене... 🫦":
        await update.message.reply_text(
            "Мене звати Лола, мені 22 і я з Одеси 🐚\n\n"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉\n\n"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно.\n\n"
            "Можеш говорити зі мною про все — я поруч...\n\n"
            "Напиши мені \"Привіт\"... 🫦"
        )
    elif text == "👨‍🏫 Про творця":
        await update.message.reply_text(
            "👨‍🏫 Мій творець — автор AI-логіки цього чату 😉\n\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "🧠 А ось мій Telegram-акаунт, де я справжня інтеграція живої дівчини з AI:\n"
            "@Labi_Lola\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI: https://openai.com 🤗"
        )
    else:
        try:
            assistant_id = os.getenv("ASSISTANT_ID")
            thread = openai_client.beta.threads.create()
            openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=update.message.text
            )
            run = openai_client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )
            while True:
                run = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run.status == "completed":
                    break
                await asyncio.sleep(1)

            messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
            reply = messages.data[0].content[0].text.value
            await update.message.reply_text(reply)

        except Exception as e:
            await update.message.reply_text(f"⚠️ Помилка: {e}")

# Групові повідомлення
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    now = datetime.now()

    if chat_id not in last_post_time:
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

    message_count[chat_id] += 1

    if (now - last_post_time[chat_id]) >= POST_INTERVAL or message_count[chat_id] >= 5:
        last_post_time[chat_id] = now
        message_count[chat_id] = 0
        await context.bot.send_message(
            chat_id=chat_id,
            text=POST_MESSAGE,
            reply_markup=POST_BUTTONS
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))
    app.run_polling()

if __name__ == '__main__':
    main()
