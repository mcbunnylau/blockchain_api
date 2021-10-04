from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from data_fetch import fetcher


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetcher.update_block, 'interval', seconds=60)
    scheduler.start()
