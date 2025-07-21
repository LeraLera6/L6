import logging
import os
import asyncio
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

# --- START: AI Thread Memory Management ---
user_threads = {}
user_histories = {}
ai_message_ids = {}
bot_message_history = {}
user_sessions = {}  # user_id: {thread_id, history, has_greeted, has_told_story, message_count}
# --- END: AI Thread Memory Management ---

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = (
    "👋 Я рада тебе тут бачити 💓\n\n"
    "Ти можеш вибрати одну з моїх подруг для більш пікантного спілкування…\n"
    "Натисни кнопку нижче ⬇️\n\n"
    "Або напиши мені в особисті повідомлення.\n\n"
    "Я чекаю... 🫦\n\n"
    "⬇️ нова версія в л.с V3.1 ⬇️"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("Напиши мені... 🫦", url="https://t.me/LOLA_A1_bot")]
])

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
        await update.message.reply_text("""🔅Тут я AI-версія Лоли (v3.1)

🔸️ Ти можеш поспілкуватись зі мною тут як з AI подругою..
🔸️ Або написати на мій основний акаунт: @Labi_Lola 🧪💞
🔸️ Також можеш натиснути одну з кнопок нижче

🔶 Або просто напиши мені
-ПРИВІТ-""", reply_markup=keyboard)

async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    # Кнопки
    KNOWN_BUTTONS = {
        "📩 Напиши мені в ЛС... 🧪💞": "👉 https://t.me/Labi_Lola",
        "🔞 Мій канал передпоказу 🧪💞": "👉 https://t.me/+rKgDRzE3wLoyYTQy",
        "👩‍🦰 Про мене... 🫦": (
            "👠 Я — Лола.. Люблю Одесу — її нічне море, солоний вітер і теплі погляди незнайомців...🫣 "
            "У цьому боті я — твоя AI-дівчина… Чуттєва, трохи небезпечна, дуже справжня ...🫦 "
            "Напиши мені \"Привіт\" — і побачиш, яка я на смак... 😈"
        ),
        "👨‍🏫 Про творця 🦾": (
            "👨‍🏫 🦾 Мій творець AI-версії — @nikita_onoff 🔅 "
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉 "
            "(Хоча якщо чесно — це він мене попросив так написати 😅)"
        )
    }

    if text in KNOWN_BUTTONS:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        except:
            pass
        msg = await context.bot.send_message(chat_id, KNOWN_BUTTONS[text])
        return

    # Сесія користувача
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "thread_id": openai_client.beta.threads.create().id,
            "history": [],
            "has_greeted": False,
            "has_told_story": False,
            "message_count": 0
        }

    session = user_sessions[user_id]
    session["message_count"] += 1
    now = datetime.now()

    # Додаємо тільки історію
    for user_msg, bot_reply, _ in session["history"][-6:]:
        openai_client.beta.threads.messages.create(
            thread_id=session["thread_id"],
            role="user",
            content=user_msg
        )
        openai_client.beta.threads.messages.create(
            thread_id=session["thread_id"],
            role="assistant",
            content=bot_reply
        )

    # Додаємо поточне повідомлення після run
    run = openai_client.beta.threads.runs.create(
        thread_id=session["thread_id"],
        assistant_id=ASSISTANT_ID
    )

    # Поточне повідомлення
    openai_client.beta.threads.messages.create(
        thread_id=session["thread_id"],
        role="user",
        content=text
    )

    while True:
        run = openai_client.beta.threads.runs.retrieve(thread_id=session["thread_id"], run_id=run.id)
        if run.status == "completed":
            break
        await asyncio.sleep(1)

    messages = openai_client.beta.threads.messages.list(thread_id=session["thread_id"])
    reply = messages.data[0].content[0].text.value

    session["history"].append((text, reply, now))
    await update.message.reply_text(reply)

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
