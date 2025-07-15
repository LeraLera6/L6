import logging
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler,
)
import openai

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфігурація
BOT_TOKEN = os.getenv("BOT_TOKEN")
GPT_ID = os.getenv("GPT_ID")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V8_bot")]
])

# Обробка команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        start_text = "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити."
        "Можеш питати серйозне, грайливе або просто поговорити.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
            [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
            [InlineKeyboardButton("👥 Про мене", callback_data="about_me")],
            [InlineKeyboardButton("👨‍🏫 Про творця", callback_data="about_creator")]
        ])
    )

# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        completion = openai.ChatCompletion.create(
            model=GPT_ID,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        reply = "Ой... я трохи розгубилась. Спробуй ще раз 🫣"

    await update.message.reply_text(reply)

# Обробка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about_me":
        await query.message.reply_text("Я — Лера, твоя фліртова AI-подруга 💋")
    elif query.data == "about_creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff
"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉
"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущено")
    app.run_polling()
