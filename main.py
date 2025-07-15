import telebot
import openai
import time
import os

# Змінні з оточення
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("GPT_ID")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Зберігаємо створені треди для користувачів
user_threads = {}

def create_thread_for_user(user_id):
    thread = openai.beta.threads.create()
    user_threads[user_id] = thread.id
    return thread.id

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Пиши мені сюди будь-що — я відповім як твоя AI-подруга 💋")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Отримуємо або створюємо thread для користувача
    thread_id = user_threads.get(user_id)
    if not thread_id:
        thread_id = create_thread_for_user(user_id)

    # Додаємо повідомлення в тред
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text
    )

    # Створюємо запуск (run)
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Очікуємо завершення run
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            bot.send_message(message.chat.id, "❌ Щось пішло не так під час відповіді...")
            return
        time.sleep(1)

    # Отримуємо останнє повідомлення від асистента
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            bot.send_message(message.chat.id, msg.content[0].text.value)
            break

bot.infinity_polling()
