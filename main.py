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
openai_client = AsyncOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=None,
    project=os.getenv("OPENAI_GPT_ID")
)

# Telegram токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Автопостинг
last_post_time = {}
message_count = {}
POST_INTERVAL = timedelta(minutes=30)
POST_MESSAGE = "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг."
POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("💞 Подружки для спілкування", url="https://t.me/virt_chat_ua1/134421")],
    [InlineKeyboardButton("❓ Задай мені питання ↗️", url="https://t.me/Lera_V8_bot")]
])

# Стартове меню в ЛС
MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("💞 Подружки для спілкування", callback_data="girls")],
    [InlineKeyboardButton("🔞 Заглянь у чат 18+", callback_data="chat18")],
    [InlineKeyboardButton("💬 Задай мені питання", callback_data="ask")],
    [InlineKeyboardButton("🧑‍🏫 Про творця", callback_data="creator")],
    [InlineKeyboardButton("🧠 Що я вмію", callback_data="skills")]
])

START_TEXT = "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋\nМожеш питати серйозне, грайливе або просто поговорити."

# Обробка кнопок у ЛС
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# Відповідь GPT
async def ask_gpt(message: str) -> str:
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"GPT Error: {e}")
        return "Вибач, я трохи заплуталась… 😅 Спробуй ще раз!"

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        reply = await ask_gpt(update.message.text)
        await update.message.reply_text(reply, reply_markup=MAIN_MENU)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=MAIN_MENU)

# Автопостинг у групах
async def group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_count[chat_id] = message_count.get(chat_id, 0) + 1
    now = datetime.now()
    last_time = last_post_time.get(chat_id, now - timedelta(hours=1))
    if now - last_time > POST_INTERVAL or message_count[chat_id] >= 5:
        await context.bot.send_message(chat_id=chat_id, text=POST_MESSAGE, reply_markup=POST_BUTTONS)
        last_post_time[chat_id] = now
        message_count[chat_id] = 0

# Головний запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS, group_message))
    app.run_polling()
