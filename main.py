import os
import openai
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters,
)
from datetime import datetime, timedelta

openai.api_key = os.environ.get("OPENAI_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Для автопостингу в чатах
last_post_time = {}
message_count = {}

# Повідомлення для груп
def get_group_message():
    keyboard = [
        [
            InlineKeyboardButton("💞 Мої подружки", url="https://t.me/virt_chat_ua1/134421"),
            InlineKeyboardButton("💬 Задай мені питання ↗️", url="https://t.me/Lera_V8_Bot"),
        ]
    ]
    return "Привіт, я Лера 😇\nЯ можу допомогти тобі в цьому світі бажань, флірту та AI-спокуси...", InlineKeyboardMarkup(keyboard)

# Привітання в ЛС
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    keyboard = [
        [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="friends")],
        [InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat18")],
        [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
        [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
        [InlineKeyboardButton("🧠 Що я вмію", callback_data="abilities")],
    ]
    await update.message.reply_text(
        "Привіт, я Лера 😇\nМені 22, я з Одеси.\nМожу поговорити, допомогти, поспілкуватись або… спокусити 🫦\n\nОбери, з чого хочеш почати:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Обробка кнопок у ЛС
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "friends":
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
        context.user_data["mode"] = "chat"
    elif query.data == "creator":
        await query.message.reply_text(
            "👨‍🏫 Мій творець — @nikita_onoff\nНестандартний, точний, ідеаліст з добрим серцем і хитрим поглядом 😉\n(Хоча якщо чесно — це він мене попросив так написати 😅)\n\n💡 Усе це — частина проєкту brEAst, створеного з ідеєю поєднати AI, спокусу та свободу спілкування.\n\n🤖 А ще я ожила завдяки магії OpenAI. Дякую їм за це 🫶"
        )
    elif query.data == "abilities":
        await query.message.reply_text(
            "Я вмію:\n— відповідати на складні питання\n— допомагати з текстами, думками, ідеями\n— фліртувати ніжно або з вогником 😉\n— і ще багато чого — просто напиши 💬"
        )

# GPT-відповідь у ЛС
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await handle_group(update, context)
        return

    if context.user_data.get("mode") != "chat":
        return

    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Щось пішло не так. 😥")

# Автопостинг у групах
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    now = datetime.now()

    # ініціалізація
    if chat_id not in last_post_time:
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

    message_count[chat_id] += 1

    if (
        message_count[chat_id] >= 5
        or (now - last_post_time[chat_id]) >= timedelta(minutes=30)
    ):
        text, keyboard = get_group_message()
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

# Запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
