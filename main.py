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
    "👋 Я рада тебе тут бачити 😊\n\n"
    "Ти можеш вибрати одну з моїх подруг для більш пікантного спілкування…\n"
    "Натисни кнопку нижче 🔝\n\n"
    "Або напиши мені в особисті повідомлення.\n\n"
    "Я чекаю... 🪦"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("Напиши мені... 🪦", url="https://t.me/Lera_v10_bot")]
])

# Команда /start — особисті повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await context.bot.delete_my_commands()
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                ["\ud83d\udc95 Подружки для спілкування \ud83d\udd1e"],
                ["\ud83d\ude08 Заглянь у чат \ud83d\udd1e"],
                ["\ud83d\udc69‍\ud83e\uddec Про мене... 🪦"],
                ["\ud83d\udc68‍\ud83c\udfeb Про творця"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
        await update.message.reply_text(
            "Привіт, я рада, що ти мені написав. Я так цього чекала...\n\n"
            "Ти можеш перейти за кнопками нижче або просто напиши мені \"Привіт\"... 🪦",
            reply_markup=keyboard
        )

# Обробка reply-кнопок в ЛС
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "\ud83d\udc95 Подружки для спілкування \ud83d\udd1e":
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        await update.message.reply_text(
            "\u0423 \u043c\u0435\u043d\u0435 \u0454 \u043f\u043e\u0434\u0440\u0443\u0433\u0438, \u044f\u043a\u0456 \u0433\u043e\u0442\u043e\u0432\u0456 \u043d\u0430 \u0431\u0456\u043b\u044c\u0448\u0435\u2026\n\n"
            "\ud83d\udc8b \u041e\u0431\u0435\u0440\u0438 \u0441\u0432\u043e\u044e \u0437\u0430 \u043d\u0430\u0441\u0442\u0440\u043e\u0454\u043c \u2014 \u043e\u0441\u044c \u043d\u0430\u0448 \u0441\u043f\u0438\u0441\u043e\u043a:\n\n"
            "\ud83d\udc49 https://t.me/virt_chat_ua1/134421"
        )
    elif text == "\ud83d\ude08 Заглянь у чат \ud83d\udd1e":
        await update.message.reply_text(
            "Там усе трохи інакше…\n\n"
            "🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n\n"
            "🕉 https://t.me/+d-pPVpIW-UBkZGUy"
        )
    elif text == "\ud83d\udc69‍\ud83e\uddec Про мене... 🪦":
        await update.message.reply_text(
            "Мене звати Лера, мені 22 і я з Одеси \ud83d\udc1a\n\n"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові \u2014 може, ти мені розкажеш більше?.. \ud83d\ude09"
        )
    elif text == "\ud83d\udc68‍\ud83c\udfeb Про творця":
        await update.message.reply_text(
            "\ud83d\udc68‍\ud83c\udfeb Мій творець — @nikita_onoff\n\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом \ud83d\ude09\n\n"
            "\u2728 Усе це — частина проєкту brEAst: https://t.me/virt_chat_ua1"
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
            await update.message.reply_text(f"\u26a0\ufe0f \u041f\u043e\u043c\u0438\u043b\u043a\u0430: {e}")

# Обробка групового чату — автопостинг
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

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, reply_to_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))
    app.run_polling()

if __name__ == '__main__':
    main()
