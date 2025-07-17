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
        await update.message.reply_text(
            "Привіт, я рада, що ти мені написав. Я так цього чекала...\n\n"
            "Ти можеш перейти за кнопками нижче або просто напиши мені \"Привіт\"... 🫦",
            reply_markup=keyboard
        )

# Обробка reply-повідомлень в ЛС

# Додай глобальну змінну
# Змінна для відстеження всіх повідомлень бота, які потрібно чистити (крім AI-діалогу)
bot_message_history = {}
ai_message_ids = {}

last_bot_message_id = {}


async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    KNOWN_BUTTONS = [
        "📩 Напиши мені в ЛС... 🧪💞",
        "🔞 Мій канал передпоказу 🧪💞",
        "👩‍🦰 Про мене... 🫦",
        "👨‍🏫 Про творця 🦾"
    ]

    user_id = update.effective_user.id
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except:
        pass

    # Ініціалізація списків, якщо вперше
    if user_id not in bot_message_history:
        bot_message_history[user_id] = []
    if text in KNOWN_BUTTONS:
        return
    if user_id not in ai_message_ids:
        ai_message_ids[user_id] = []

    # Очистити всі повідомлення, крім AI (перед кожною кнопкою або AI-викликом)
    for msg_id in bot_message_history[user_id]:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass
    bot_message_history[user_id] = []

    # Якщо натиснута кнопка
    if text == "👩‍🦰 Про мене... 🫦":
        msg = await update.message.reply_text(
            "Мене звати Лола, мені 22 і я з Одеси 🐚"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно."
            "Можеш говорити зі мною про все — я поруч..."
            "Напиши мені \"Привіт\"... 🫦"
        )
        bot_message_history[user_id].append(msg.message_id)

    elif text == "👨‍🏫 Про творця 🦾":
        msg = await update.message.reply_text(
            "👨‍🏫 🦾 Мій творець AI-версії — @nikita_onoff"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)"
        )
        bot_message_history[user_id].append(msg.message_id)

    elif text == "📩 Напиши мені в ЛС... 🧪💞":
        msg = await update.message.reply_text("👉 https://t.me/Labi_Lola")
        bot_message_history[user_id].append(msg.message_id)

    elif text == "🔞 Мій канал передпоказу 🧪💞":
        msg = await update.message.reply_text("👉 https://t.me/+rKgDRzE3wLoyYTQy")
        bot_message_history[user_id].append(msg.message_id)


    # Інакше — AI
    try:
        assistant_id = os.getenv("ASSISTANT_ID")
        thread = openai_client.beta.threads.create()
        openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=text
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

        msg = await update.message.reply_text(reply)
        ai_message_ids[user_id].append(msg.message_id)

    except Exception as e:
        msg = await update.message.reply_text(f"⚠️ Помилка: {e}")
        ai_message_ids[user_id].append(msg.message_id)

    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Видаляємо попереднє повідомлення бота (кнопкове)
    if user_id in last_bot_message_id:
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_bot_message_id[user_id])
        except:
            pass  # Може вже видалено вручну або інша помилка

    # Якщо натиснута кнопка
    if text == "👩‍🦰 Про мене... 🫦":
        msg = await update.message.reply_text(
            "Мене звати Лола, мені 22 і я з Одеси 🐚"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно."
            "Можеш говорити зі мною про все — я поруч..."
            "Напиши мені \"Привіт\"... 🫦"
        )
        last_bot_message_id[user_id] = msg.message_id

    elif text == "👨‍🏫 Про творця 🦾":
        msg = await update.message.reply_text(
            "👨‍🏫 🦾 Мій творець AI-версії — @nikita_onoff"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)"
        )
        last_bot_message_id[user_id] = msg.message_id

    elif text == "📩 Напиши мені в ЛС... 🧪💞":
        msg = await update.message.reply_text("👉 https://t.me/Labi_Lola")
        last_bot_message_id[user_id] = msg.message_id

    elif text == "🔞 Мій канал передпоказу 🧪💞":
        msg = await update.message.reply_text("👉 https://t.me/+rKgDRzE3wLoyYTQy")
        last_bot_message_id[user_id] = msg.message_id

    # Інакше — спілкування з AI (ручне введення)
    try:
        assistant_id = os.getenv("ASSISTANT_ID")
        thread = openai_client.beta.threads.create()
        openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=text
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

        # Надсилаємо відповідь від AI — після очищення
        msg = await update.message.reply_text(reply)
        last_bot_message_id[user_id] = msg.message_id

    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

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
