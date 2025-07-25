import os
import time
from datetime import datetime, timedelta, timezone, time as dtime
from zoneinfo import ZoneInfo  # Python 3.9+
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

KYIV_TZ = ZoneInfo("Europe/Kyiv")

# ---------------------- helpers ---------------------- #

def send(text: str):
    try:
        bot.send_message(chat_id=LOG_CHAT_ID, text=text[:4096])  # на всякий
    except Exception as e:
        # останній шанс – спробувати хоч щось вивести
        try:
            bot.send_message(chat_id=LOG_CHAT_ID, text=f"❌ Помилка при надсиланні звіту: {e}")
        except:
            pass

def read_last_lines(path: str, n: int = 200) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[-n:]) if lines else "Лог порожній."
    except Exception as e:
        return f"⚠️ Не вдалося прочитати лог: {e}"

def build_hourly_report() -> str:
    logs = read_last_lines("ai_interactions.log", 80)
    now_k = datetime.now(KYIV_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"⏱️ Щогодинний звіт ({now_k})\n\n{logs}"

def build_daily_report() -> str:
    logs = read_last_lines("ai_interactions.log", 400)
    now_k = datetime.now(KYIV_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")
    return f"📊 Добовий звіт ({now_k}) — за останні 24 години\n\n{logs}"

def next_kyiv_23_utc() -> datetime:
    """Розрахувати найближчі 23:00 за Києвом та повернути час у UTC."""
    now_k = datetime.now(KYIV_TZ)
    today_23 = datetime.combine(now_k.date(), dtime(23, 0, 0), tzinfo=KYIV_TZ)
    if now_k >= today_23:
        target_k = today_23 + timedelta(days=1)
    else:
        target_k = today_23
    return target_k.astimezone(timezone.utc)

# ---------------------- main loop ---------------------- #

def hourly_report_loop():
    """
    1) Перший репорт — через 20 хв після запуску
    2) Потім — щогодини
    3) О 23:00 за Києвом — добовий звіт
    """
    start_utc = datetime.now(timezone.utc)
    first_send_at = start_utc + timedelta(minutes=20)
    first_sent = False

    next_hourly = None
    next_daily_utc = next_kyiv_23_utc()

    send("🟢 Звітність запущена. Перший звіт буде через 20 хвилин, далі — щогодини. Добовий о 23:00 за Києвом.")

    while True:
        try:
            now_utc = datetime.now(timezone.utc)

            # Перший (через 20 хв)
            if not first_sent and now_utc >= first_send_at:
                send(build_hourly_report())
                first_sent = True
                next_hourly = now_utc + timedelta(hours=1)

            # Щогодинні
            if first_sent and next_hourly and now_utc >= next_hourly:
                send(build_hourly_report())
                next_hourly = next_hourly + timedelta(hours=1)

            # Добовий 23:00 за Києвом
            if now_utc >= next_daily_utc:
                send(build_daily_report())
                next_daily_utc = next_kyiv_23_utc()

        except Exception as e:
            # щоб потік не падав
            try:
                send(f"❗️Помилка у звітному циклі: {e}")
            except:
                pass

        time.sleep(10)  # перевіряємо події кожні 10 секунд
