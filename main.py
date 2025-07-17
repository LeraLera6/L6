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
    "<b>👋 Я рада тебе тут бачити…</b>

"
    "<b>Ти можеш вибрати одну з моїх подруг для більш пікантного спілкування…</b>
"
    "<b>Натисни кнопку нижче 🖤</b>

"
    "<b>Або напиши мені в особисті повідомлення.</b>

"
    "<b>Я чекаю... 🫦</b>"
)
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування 🔞", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("Напиши мені... 🫦", url="https://t.me/Lera_v10_bot")]
])

# Команда /start — особисті повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                ["💞 Подружки для спілкування 🔞"],
                ["😈 Заглянь у чат 🔞"],
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
    try:
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    except:
        pass
    text = update.message.text.strip()
    if text == "👩‍🦰 Про мене... 🫦":
        await update.message.reply_text(
            "Мене звати Лера, мені 22 і я з Одеси 🐚\n\n"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉\n\n"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно.\n\n"
            "Можеш говорити зі мною про все — я поруч...\n\n"
            "Напиши мені \"Привіт\"... 🫦"
        )
    elif text == "👨‍🏫 Про творця":
        await update.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту brEAst: https://t.me/virt_chat_ua1\n\n"
            "🤖 А ще я ожила завдяки магії OpenAI: https://openai.com 🤗"
        )
    elif text == "💞 Подружки для спілкування 🔞":
        await update.message.reply_text(
            "У мене є подруги, які готові на більше…\n\n"
            "💋 Обери свою за настроєм — ось наш список:\n\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )
    elif text == "😈 Заглянь у чат 🔞":
        await update.message.reply_text(
            "Там усе трохи інакше…\n\n"
            "🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n\n"
            "👉 https://t.me/+d-pPVpIW-UBkZGUy"
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
            # Очікування завершення run
            while True:
                run = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run.status == "completed":
                    break
                await asyncio.sleep(1)

            messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
            reply = messages.data[0].content[0].text.value
                    try:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass

        await update.message.reply_text(reply)

        except Exception as e:
            await update.message.reply_text(f"⚠️ Помилка: {e}")

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
