import os
import openai
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime

# ініціалізація клієнта OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# словники для автопостингу
last_post_time = {}
message_count = {}

# кнопки для ЛС
private_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("💕 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("🔞 Заглянь у чат 18+", url="https://t.me/+d-pPVpIW-UBkZGUy")],
    [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask_question")],
    [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="about_creator")],
    [InlineKeyboardButton("🧠 Що я вмію", callback_data="what_i_can")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт, я Лера 😇\nМенi 22, я з Одеси.\nМожу поговорити, допомогти, поспілкуватись або... спокусити 💋\n\nОбери, з чого хочеш почати:",
        reply_markup=private_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Помилка:\n\n{str(e)}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about_creator":
        await query.edit_message_text(
            "\U0001F468‍\U0001F3EB Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n💡 Усе це — частина проєкту [brEAst](https://t.me/+d-pPVpIW-UBkZGUy), створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶",
            disable_web_page_preview=True
        )
    elif query.data == "what_i_can":
        await query.edit_message_text(
            "Я вмію:\n— відповідати на складні питання\n— допомагати з текстами, думками, ідеями\n— фліртувати ніжно або з вогником 😉\n— і ще багато чого — просто напиши 💬"
        )
    elif query.data == "ask_question":
        await query.edit_message_text(
            "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити."
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
