import logging
import openai
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from datetime import datetime, timedelta

# Увімкнення логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Отримання токенів із змінних середовища
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Привітальне повідомлення та кнопки
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")],
        [InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat18")],
        [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
        [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
        [InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привіт, я Лера 😇\nМені 22, я з Одеси.\nМожу поговорити, допомогти, поспілкуватись або… спокусити 💋\n\nОбери, з чого хочеш почати:",
        reply_markup=reply_markup
    )

# Обробка натискань кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "girls":
        await query.message.reply_text(
            "У мене є подруги, які готові на більше…\n💋 Обери свою за настроєм — ось наш список:\n👉 https://t.me/virt_chat_ua1/134421"
        )
    elif query.data == "chat18":
        await query.message.reply_text(
            "Там усе трохи інакше…\n🔞 Відверті розмови, інтимні жарти, і я в трохи іншому образі 😈\n👉 https://t.me/+d-pPVpIW-UBkZGUy"
        )
    elif query.data == "ask":
        await query.message.reply_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити."
        )
    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )
    elif query.data == "skills":
        await query.message.reply_text(
            "Я вмію:\n— відповідати на складні питання\n— допомагати з текстами, думками, ідеями\n— фліртувати ніжно або з вогником 😉\n— і ще багато чого — просто напиши 💬"
        )

# Обробка повідомлень у ЛС
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка: {e}")

# Автопостинг у групах
last_post_time = {}
message_count = {}

async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    now = datetime.now()

    if chat_id not in last_post_time:
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

    message_count[chat_id] += 1
    time_diff = now - last_post_time[chat_id]

    if message_count[chat_id] >= 5 or time_diff >= timedelta(minutes=30):
        keyboard = [
            [
                InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")
            ],
            [
                InlineKeyboardButton("❓ Задай мені питання ↗️", url=f"https://t.me/{context.bot.username}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг.",
            reply_markup=reply_markup
        )
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))
    app.run_polling()
