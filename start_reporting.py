import threading
from reporting_task import hourly_report_loop

def start_reporting_thread():
    t = threading.Thread(target=hourly_report_loop, daemon=True)
    t.start()
