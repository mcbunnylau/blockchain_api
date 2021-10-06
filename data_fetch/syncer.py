from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from data_fetch.fetcher import daily_sync


def start():
    scheduler = BackgroundScheduler()
    print("starting....")
    scheduler.add_job(daily_sync, trigger="cron",
                      hour=2, minute=5, second=40)
    print("job added")
    scheduler.start()
