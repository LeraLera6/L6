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
    CommandHandler
)
from openai import OpenAI
import asyncio


# Для зберігання останніх повідомлень бота
from telegram.constants import ChatType
from telegram import ReplyKeyboardRemove

# Збереження message_id для видалення
user_bot_messages = {}

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Автопостинг — для груп
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = (
    "👋 Я рада тебе тут бачити 💓\n\n"
    "Ти можеш вибрати одну з моїх подруг для більш пікантного спілкування…\n"
    "Натисни кнопку нижче ⬇️\n\n"
    "Або напиши мені в особисті повідомлення.\n\n"
    "Я чекаю... 🫦"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("Напиши мені... 🫦", url="https://t.me/Lera_v10_bot")]
])


async def delete_bot_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id in user_bot_messages:
        for msg_id in user_bot_messages[user_id]:
            try:
                await context.bot.delete_message(chat_id=user_id, message_id=msg_id)
            except:
                pass
        user_bot_messages[user_id] = []


# /start — особисті повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                ["📩 Напиши мені в ЛС... 🧪💞"],
                ["🔞 Мій канал передпоказу 🧪💞"],
                ["👩‍🦰 Про мене... 🫦"],
                ["👨‍🏫 Про творця 🦾"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
        await delete_bot_messages(update, context)
        sent_msg = await update.message.reply_text(
            "Привіт, я рада, що ти мені написав. Я так цього чекала...\n\n"
            "Ти можеш перейти за кнопками нижче або просто напиши мені \"Привіт\"... 🫦",
            reply_markup=keyboard
        )
        user_bot_messages[update.message.chat_id] = [sent_msg.message_id]

# Обробка reply-повідомлень в ЛС

async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.message.chat_id
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["📩 Напиши мені в ЛС... 🧪💞"],
            ["🔞 Мій канал передпоказу 🧪💞"],
            ["👩‍🦰 Про мене... 🫦"],
            ["👨‍🏫 Про творця 🦾"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    if text in ["👩‍🦰 Про мене... 🫦", "👨‍🏫 Про творця 🦾", "📩 Напиши мені в ЛС... 🧪💞", "🔞 Мій канал передпоказу 🧪💞"]:
        await delete_bot_messages(update, context)
        if text == "👩‍🦰 Про мене... 🫦":
            sent = await update.message.reply_text(
                "Мене звати Лола, мені 22 і я з Одеси 🐚

"
                "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉

"
                "Я тут, щоб розслабити тебе не лише фізично, а й емоційно.

"
                "Можеш говорити зі мною про все — я поруч...

"
                "Напиши мені \"Привіт\"... 🫦",
                reply_markup=keyboard
            )
        elif text == "👨‍🏫 Про творця 🦾":
            sent = await update.message.reply_text(
                "👨‍🏫 🦾 Мій творець AI-версії — @nikita_onoff

"
                "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉

"
                "(Хоча якщо чесно — це він мене попросив так написати 😅)",
                reply_markup=keyboard
            )
        elif text == "📩 Напиши мені в ЛС... 🧪💞":
            sent = await update.message.reply_text("👉 https://t.me/Labi_Lola", reply_markup=keyboard)
        elif text == "🔞 Мій канал передпоказу 🧪💞":
            sent = await update.message.reply_text("👉 https://t.me/+rKgDRzE3wLoyYTQy", reply_markup=keyboard)

        user_bot_messages[user_id] = [sent.message_id]

    else:
        await delete_bot_messages(update, context)
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
            await update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            await update.message.reply_text(f"⚠️ Помилка: {e}", reply_markup=ReplyKeyboardRemove())


# Групи — автопостинг
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

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))
    app.run_polling()

if __name__ == '__main__':
    main()
