import logging
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CommandHandler
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
POST_MESSAGE = ("Привіт, я рада тебе тут бачити.
""Ти можеш вибрати одну з моїх подруг для більш пікантного спілкування.
""Або напиши мені в особисті повідомлення.
""Я чекаю... 🫦")
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
            "👨‍🏫 Мій творець — [@nikita_onoff](https://t.me/nikita_onoff)\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶",
            parse_mode="Markdown"
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

# GPT-чат
async def reply_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    try:
        response = await openai_client.chat.completions.create(
        assistant_id=os.getenv("ASSISTANT_ID"),
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": update.message.text}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
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




from telegram import ReplyKeyboardMarkup

# Обробка команд та кнопок у ЛС (з ReplyKeyboardMarkup)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "Привіт, я рада, що ти мені написав. Я так цього чекала...
"
        "Ти можеш перейти за кнопками нижче або просто напиши мені \"Привіт\"... 🫦",
        reply_markup=keyboard
    )


def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "about_me":
        await query.edit_message_text(
            "Мене звати Лера, мені 22 і я з Одеси 🐚\n"
            "Я вивчала психологію і трохи знаюся на тому, що у тебе в голові 😉\n\n"
            "Я тут, щоб розслабити тебе не лише фізично, а й емоційно.\n"
            "Можеш говорити зі мною про все — я поруч...\n"
            "Напиши мені \"Привіт\"... 🫦"
        )
    elif query.data == "about_creator":
        await query.edit_message_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту brEAst: https://t.me/virt_chat_ua1\n"
            "🤖 А ще я ожила завдяки магії OpenAI: https://openai.com 🤗"
        )

# Реєстрація хендлерів
def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
