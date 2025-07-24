import os
import asyncio
from datetime import datetime
from telegram import Bot

LOG_CHAT_ID = os.getenv("LOG_CHANNEL_ID")  # ID чата логів
LOG_FILE_PATH = "ai_interactions.log"      # Шлях до лог-файлу

async def report_loop():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    while True:
        now = datetime.now()
        if os.path.exists(LOG_FILE_PATH):
            try:
                with open(LOG_FILE_PATH, "rb") as log_file:
                    await bot.send_document(
                        chat_id=LOG_CHAT_ID,
                        document=log_file,
                        filename=f"log_{now.strftime('%Y-%m-%d_%H-%M')}.txt",
                        caption=f"🧾 Лог за {now.strftime('%H:%M')}"
                    )
            except Exception as e:
                print(f"[report_loop] error: {e}")
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(report_loop())
