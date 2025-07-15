import logging
import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from openai import AsyncOpenAI

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI ініціалізація
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Для автопостінгу
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

# Відповіді на кнопки в ЛС
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ask":
        context.user_data["chat_mode"] = True
        await query.message.reply_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )
    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )
    elif query.data == "skills":
        await query.message.reply_text(
            "Я вмію:\n"
            "— відповідати на складні питання\n"
            "— допомагати з текстами, думками, ідеями\n"
            "— фліртувати ніжно або з вогником 😉\n"
            "— і ще багато чого — просто напиши 💬"
        )
    elif query.data == "girls":
        await query.message.reply_text(
            "У мене є подруги, які готові на більше…\n"
            "💋 Обери свою за настроєм — ось наш список:\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")],
                [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
                [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
                [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
                [InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")]
            ])
        )

# Основна логіка відповіді в ЛС
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    if not context.user_data.get("chat_mode", False):
        return
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": update.message.text}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# Автопостинг у групах без відповіді на користувачів
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

# Хендлери
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

    app.run_polling()

if __name__ == '__main__':
    main()

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
