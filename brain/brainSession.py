from brainTools import query_token
from apscheduler.schedulers.background import BackgroundScheduler


brain_token = query_token('brain')

scheduler = BackgroundScheduler(misfire_grace_time=60)
