import logging
import os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

START_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")],
    [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
    [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
    [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
])

START_MESSAGE = "Я знаю, чим тебе зацікавити 😉 Обирай одну з кнопок нижче та занурюйся..."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE, reply_markup=START_KEYBOARD)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "girls":
        await query.message.reply_text(
            "У мене є подруги, які готові на більше…\n"
            "💋 Обери свою за настроєм — ось наш список:\n"
            "👉 https://t.me/virt_chat_ua1/134421"
        )

    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\n"
            "Нестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n"
            "(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n"
            "💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n"
            "🤖 А ще я ожила завдяки магії [OpenAI](https://openai.com). Дякую їм за це 🫶",
            parse_mode="Markdown"
        )

    elif query.data == "ask":
        await query.message.reply_text(
            "Пиши мені будь-що — я відповім як твоя AI-подруга 💋\n"
            "Можеш питати серйозне, грайливе або просто поговорити."
        )
        context.user_data['chat_mode'] = True

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('chat_mode'):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ти фліртова AI-подруга. Відповідай з ніжністю, але з інтригою."},
                    {"role": "user", "content": update.message.text},
                ]
            )
            reply_text = response.choices[0].message.content
        except Exception as e:
            reply_text = f"🔧 Щось пішло не так...\n\n```
{e}
```"
        await update.message.reply_text(reply_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "Я тут, щоб фліртувати та спілкуватись. Натисни кнопку нижче, щоб почати!",
            reply_markup=START_KEYBOARD
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()
