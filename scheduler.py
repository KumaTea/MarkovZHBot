from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(misfire_grace_time=60)