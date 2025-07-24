from reporting_task import hourly_report_loop

def start_reporting_thread():
    import threading
    thread = threading.Thread(target=hourly_report_loop, daemon=True)
    thread.start()
