import logging
import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, filters,
    CallbackQueryHandler, CommandHandler
)
from openai import AsyncOpenAI

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
POST_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421"),
        InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V4bot")
    ]
])

# Обробка callback-кнопок у ЛС
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ask":
        await query.message.reply_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )
    elif query.data == "girls":
        await query.message.reply_text(
            "У мене є подруги, які готові на більше… 💋\n👉 https://t.me/virt_chat_ua1/134421"
        )
    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "💡 Це все частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n"
            "🤖 Я ожила завдяки [OpenAI](https://openai.com/) 🫶",
            parse_mode="Markdown"
        )

# Команда /start у ЛС
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "Привіт 😘 Я Лера. Пиши мені що завгодно або обери кнопку:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")],
                [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
                [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
                [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")]
            ])
        )

# Відповідь в ЛС через GPT
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": update.message.text}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# Автопостинг у групах
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

# Основна логіка
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

    app.run_polling()

if __name__ == '__main__':
    main()
