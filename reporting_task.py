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
    logs = read_last_lines("user_stats.log", 400)
    now_k = datetime.now(KYIV_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

    users = {}
    ai_users = {}

    for line in logs.splitlines():
        if "—" in line:
            parts = line.split("—")
            if len(parts) >= 3:
                user_id = parts[1].strip()
                action = parts[2].strip()

                if "AI" in action:
                    if user_id not in ai_users:
                        ai_users[user_id] = []
                    if len(ai_users[user_id]) < 4:
                        ai_users[user_id].append(action)
                else:
                    if user_id not in users:
                        users[user_id] = []
                    if len(users[user_id]) < 4:
                        users[user_id].append(action)

    body = f"⏱️ Щогодинний звіт ({now_k})\n\n"
    body += f"👥 Унікальних користувачів (взаємодія з ботом): {len(users)}\n"
    body += f"🤖 AI-взаємодій (унікальних юзерів): {len(ai_users)}\n\n"

    body += "📋 Останні події:\n"
    for user_id, actions in users.items():
        for a in actions:
            body += f"{user_id} — {a}\n"
    for user_id, actions in ai_users.items():
        for a in actions:
            body += f"{user_id} — {a}\n"

    return body[:4096]

def build_daily_report() -> str:
    return build_hourly_report()

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
