from tgapi import Bot
from botInfo import self_id
from apscheduler.schedulers.background import BackgroundScheduler


bot = Bot(self_id)

scheduler = BackgroundScheduler(misfire_grace_time=60)
