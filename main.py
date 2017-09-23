from apscheduler.schedulers.background import BackgroundScheduler
from db import Session
from jobs.article import updateArticleJob, crawlNewArticleJob
import time

import logging
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scheduler = BackgroundScheduler()


# scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.add_job(crawlNewArticleJob, name='crawlNewArticleJob', trigger='interval', minutes=1)
scheduler.add_job(updateArticleJob, name='updateArticleJob', trigger='cron', hour='*/1')
scheduler.start()

while True:
  time.sleep(2)
