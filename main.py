from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging
import os

BOT_USERNAME = "LERA_V6_bot"
MY_NICK = "@nikita_onoff"
MODELS_LINK = "https://t.me/virt_chat_ua1/134421"
CHAT_LINK = "https://t.me/+d-pPVpIW-UBkZGUy"
LOG_CHAT_ID = -1002122539626  # Чат для логів

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Поведінка Лери ---
RESPONSES = {
    "hello": [
        "Привіт, сонце ☀️ Я тут... А ти шукав мене? 😌",
        "Ммм, я тільки з’явилась... Ти мене кликав? 😇",
        "О, ти знову тут? Я тебе вже почала чекати 😉"
    ],
    "repeat": [
        "Мені здається, я вже відповідала 😌",
        "Я не готова зараз повторюватися…",
        "Може, спробуємо щось нове?..",
        "Я трохи втомилась, але я все ще тут…"
    ]
}

# --- Кнопки ---
def get_ls_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Мої подружки для спілкування зараз 💋", url=MODELS_LINK)],
        [InlineKeyboardButton("Про мене 🧠", callback_data="about_me")],
        [InlineKeyboardButton("Ціль проєкту 🎯", callback_data="project_goal")],
        [InlineKeyboardButton("Про мого творця 💼", callback_data="about_creator")]
    ])

def get_group_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Мої подружки для спілкування зараз 💋", url=MODELS_LINK),
            InlineKeyboardButton("Задай мені питання 💌", url=f"https://t.me/{BOT_USERNAME}")
        ]
    ])

# --- Обробники ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привіт, {name} 😘 Я Лера — AI дівчина, яка любить флірт і цікаві розмови…\n"
        "Тобі буде зі мною тепло 😌\n\nОбери щось цікаве нижче:",
        reply_markup=get_ls_buttons()
    )

async def reply_to_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if BOT_USERNAME.lower() in message.text.lower():
        await message.reply_text(
            "Ой, я тут 😇 Ти кликав? Хочеш когось особливого? Обери одну з моїх подруг:",
            reply_markup=get_group_buttons()
        )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about_me":
        await query.edit_message_text(
            "Я — Лера, твоя AI-подружка 😇 Я люблю спілкуватись, фліртувати і піднімати настрій.\n"
            "Хочеш дізнатись більше? Просто поговори зі мною 💬",
            reply_markup=get_ls_buttons()
        )
    elif query.data == "project_goal":
        await query.edit_message_text(
            "Цей проєкт — про спокусу, тепло, і... трохи штучного інтелекту 😉\n"
            "Я ще в процесі розвитку, але ти вже можеш отримати задоволення від нашого спілкування."
        , reply_markup=get_ls_buttons())
    elif query.data == "about_creator":
        await query.edit_message_text(
            f"Мого творця звати Нікіта. Його можна знайти тут: {MY_NICK}\n"
            "Він вкладає в мене частинку душі та фантазії 😘",
            reply_markup=get_ls_buttons()
        )

async def default_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "прив" in text or "ку" in text or "хто тут" in text:
        await update.message.reply_text(RESPONSES["hello"][0], reply_markup=get_group_buttons())
    else:
        await update.message.reply_text(
            "Я ще не знаю як відповісти 🫣 Але я можу запропонувати дещо цікаве 👇",
            reply_markup=get_group_buttons()
        )

# --- Ініціалізація ---
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, reply_to_mention))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, default_response))
app.add_handler(CallbackQueryHandler(callback_handler))

if __name__ == '__main__':
    app.run_polling()
