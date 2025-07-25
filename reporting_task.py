import os
import time
from datetime import datetime, timedelta, timezone, time as dtime
from zoneinfo import ZoneInfo
from email_sender import send_email_report

KYIV_TZ = ZoneInfo("Europe/Kyiv")

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
    now_k = datetime.now(KYIV_TZ)
    today_23 = datetime.combine(now_k.date(), dtime(23, 0, 0), tzinfo=KYIV_TZ)
    if now_k >= today_23:
        target_k = today_23 + timedelta(days=1)
    else:
        target_k = today_23
    return target_k.astimezone(timezone.utc)

def hourly_report_loop():
    start_utc = datetime.now(timezone.utc)
    first_send_at = start_utc + timedelta(minutes=20)
    first_sent = False

    next_hourly = None
    next_daily_utc = next_kyiv_23_utc()

    send_email_report("✅ Звітність запущена", "Перший звіт буде через 20 хвилин, далі — щогодини. Добовий о 23:00 за Києвом.")

    while True:
        try:
            now_utc = datetime.now(timezone.utc)

            if not first_sent and now_utc >= first_send_at:
                send_email_report("⏱️ Перший звіт", build_hourly_report())
                first_sent = True
                next_hourly = now_utc + timedelta(hours=1)

            if first_sent and next_hourly and now_utc >= next_hourly:
                send_email_report("⏱️ Щогодинний звіт", build_hourly_report())
                next_hourly = next_hourly + timedelta(hours=1)

            if now_utc >= next_daily_utc:
                send_email_report("📊 Добовий звіт", build_daily_report())
                next_daily_utc = next_kyiv_23_utc()

        except Exception as e:
            send_email_report("❗️ Помилка у звітному циклі", str(e))

        time.sleep(10)
