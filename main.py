import logging
import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler, CommandHandler
)
from openai import AsyncOpenAI

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Клієнт OpenAI
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_v10_bot")]
])

# Обробка кнопок у ЛС
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "Мене звати Лера, мені 22 і я з Одеси 🐚\n"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉\n\n"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно.\n"
            "Можеш говорити зі мною про все — я поруч 💋"
        )

    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )

    elif query.data == "girls":
        await query.message.reply_text(
            "У мене є подруги, які готові на більше…\n"
            "💋 Обери свою за настроєм — ось наш список:\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )

# Старт у ЛС
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
                [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
                [InlineKeyboardButton("👥 Про мене", callback_data="about")],
                [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")]
            ])
        )

# GPT через OpenAI Assistant
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    try:
        thread = await openai_client.beta.threads.create()
        await openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=update.message.text
        )
        run = await openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("ASSISTANT_ID")
        )
        while True:
            status = await openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if status.status == "completed":
                break
            await asyncio.sleep(1)

        messages = await openai_client.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                await update.message.reply_text(msg.content[0].text.value)
                break
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# Група — автопостинг
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
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))
    app.run_polling()

if __name__ == '__main__':
    main()
