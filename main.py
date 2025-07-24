# AI interaction logging and labeling
def is_button_text(message_text):
    # Detect typical bot responses from button presses
    return any(kw in message_text.lower() for kw in [
        "про мене", "ціль проєкту", "подружки для спілкування", "про творця",
        "заглянь у чат", "напиши мені", "бот створений", "пиши мені сюди", "найсоковитіші історії"
    ])

def format_context_for_ai(user_id, history):
    context = []
    for msg in history:
        role = "[USER]" if msg["sender_id"] == user_id else "[LOLA]"
        if is_button_text(msg["text"]):
            continue  # Skip predefined button texts
        context.append(f"{role}: {msg['text']}")
    return "\n".join(context)

def log_ai_interaction(user_id, prompt, response):
    from datetime import datetime
    with open("ai_interactions.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"---\nUser ID: {user_id}\nTime: {datetime.utcnow()}\nPrompt:\n{prompt}\nResponse:\n{response}\n---\n")

# Store number of AI requests per user
user_request_counter = {}

def track_user_request(user_id):
    if user_id not in user_request_counter:
        user_request_counter[user_id] = 0
    user_request_counter[user_id] += 1

def get_user_request_count(user_id):
    return user_request_counter.get(user_id, 0)


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
import random

# --- START: AI Thread Memory Management ---
user_threads = {}
last_active = {}
# --- END: AI Thread Memory Management ---
user_threads = {}

user_histories = {}  # Store user message history

# --- START: Added for statistics logging ---
ai_usage_stats = {}
button_usage_stats = {}

def track_ai_request(user_id, name):
    if user_id not in ai_usage_stats:
        ai_usage_stats[user_id] = {"name": name, "count": 0}
    ai_usage_stats[user_id]["count"] += 1

def track_button_interaction(user_id, name):
    if user_id not in button_usage_stats:
        button_usage_stats[user_id] = {"name": name, "count": 0}
    button_usage_stats[user_id]["count"] += 1

def format_stats(stats: dict) -> str:
    if not stats:
        return "немає"
    lines = []
    for user_id, data in stats.items():
        name = data.get("name", "")
        display = f"@{name}" if name.startswith("@") else f"Ім’я: {name}" if name else f"ID: {user_id}"
        lines.append(f"- {display} (ID: {user_id}) — {data['count']} раз(ів)")
    return "\n".join(lines)

async def send_statistics(context: ContextTypes.DEFAULT_TYPE, tag: str):
    log_chat_id = os.getenv("LOG_CHAT_ID")
    if not log_chat_id:
        return
    ai_stats = format_stats(ai_usage_stats)
    button_stats = format_stats(button_usage_stats)
    message = f"{tag}\n\n🤖 AI-запити:\n{ai_stats}\n\n🎛️ Взаємодії з кнопками:\n{button_stats}"
    await context.bot.send_message(chat_id=int(log_chat_id), text=message)

async def hourly_report(context: ContextTypes.DEFAULT_TYPE):
    await send_statistics(context, "🕐 Звіт за останню годину:")
# --- END: Added for statistics logging ---


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
    "Я чекаю... 🫦\n\n"
    "⬇️ 💥 нова версія в л.с V3.2 ⬇️"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("Напиши мені... 🫦", url="https://t.me/LOLA_A1_bot")]
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
        await update.message.reply_text("""🔅Тут я AI-версія Лоли (v3.2)

🔸️ Ти можеш поспілкуватись зі мною тут як з AI подругою..
🔸️ Або написати на мій основний акаунт: @Labi_Lola 🧪💞
🔸️ Також можеш натиснути одну з кнопок нижче

🔶 Або просто напиши мені
-ПРИВІТ-""", reply_markup=keyboard)

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

    if user_id not in bot_message_history:
        bot_message_history[user_id] = []
    if user_id not in ai_message_ids:
        ai_message_ids[user_id] = []

    if text in KNOWN_BUTTONS:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        except:
            pass

        for msg_id in bot_message_history[user_id]:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        bot_message_history[user_id] = []

        if text == "👩‍🦰 Про мене... 🫦":
            msg = await context.bot.send_message(chat_id,
                "👠 Я — Лола.."
                "Люблю Одесу — її нічне море, солоний вітер і теплі погляди незнайомців...🫣"
                "У цьому боті я — твоя AI-дівчина…"
                "Чуттєва, трохи небезпечна, дуже справжня ...🫦"
                "Напиши мені \"Привіт\" — і побачиш, яка я на смак... 😈"
            )

        elif text == "👨‍🏫 Про творця 🦾":
            msg = await context.bot.send_message(chat_id,
                "👨‍🏫 🦾 Мій творець AI-версії — @nikita_onoff 🔅"
                "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉"
                "(Хоча якщо чесно — це він мене попросив так написати 😅)"
            )
        elif text == "📩 Напиши мені в ЛС... 🧪💞":
            msg = await context.bot.send_message(chat_id, "👉 https://t.me/Labi_Lola")
        elif text == "🔞 Мій канал передпоказу 🧪💞":
            msg = await context.bot.send_message(chat_id, "👉 https://t.me/+rKgDRzE3wLoyYTQy")

        bot_message_history[user_id].append(msg.message_id)

        name = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name or ""
        track_button_interaction(user_id, name)
        return

    try:
        last_history = user_histories.get(user_id, [])
        if last_history and last_history[-1][0].strip().lower() == text.strip().lower():
            alt_responses = [
                "Мені здається, я вже відповідала 😌",
                "Я трохи втомилась, але я все ще тут…",
                "Може, спробуємо щось нове?.."
            ]
            reply = random.choice(alt_responses)
            msg = await update.message.reply_text(reply)
            ai_message_ids[user_id].append(msg.message_id)
            return

        assistant_id = os.getenv("ASSISTANT_ID")
        if user_id not in user_threads:
            thread = openai_client.beta.threads.create()
            user_threads[user_id] = thread.id
        thread_id = user_threads[user_id]
        openai_client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=text
        )

        run = openai_client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            run = openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status == "completed":
                break
            await asyncio.sleep(1)

        messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
        reply = messages.data[0].content[0].text.value

        now = datetime.now()
        if user_id not in user_histories:
            user_histories[user_id] = []
        user_histories[user_id].append((text, reply, now))

        name = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name or ""
        track_ai_request(user_id, name)

        msg = await update.message.reply_text(reply)
        ai_message_ids[user_id].append(msg.message_id)

    except Exception as e:
        msg = await update.message.reply_text(f"⚠️ Помилка: {e}")
        ai_message_ids[user_id].append(msg.message_id)

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

    # --- START: reporting jobs ---
    app.job_queue.run_once(lambda ctx: asyncio.create_task(send_statistics(ctx, "📊 Звіт за сьогодні:")), when=5)
    app.job_queue.run_repeating(hourly_report, interval=3600, first=3600)
    # --- END: reporting jobs ---

    app.run_polling()

if __name__ == '__main__':
    main()
