import time
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.article import crawlNewArticleJob, crawlArticleDetailJob, completeDetailAndSaveJob
from jobs import user as userJob, comment as commentJob

import logging
logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scheduler = BackgroundScheduler()



# scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# crawlNewArticleJob()
# crawlArticleDetailJob()

#articles
scheduler.add_job(crawlNewArticleJob, name='crawlNewArticleJob', trigger='interval', minutes=10)
scheduler.add_job(crawlArticleDetailJob, name='crawlArticleDetailJob', trigger='cron', hour='10')
scheduler.add_job(completeDetailAndSaveJob, name='completeDetailAndSaveJob', trigger='interval', minutes=10)

#users
scheduler.add_job(userJob.crwalBasicJob, name='userJob.crwalBasicJob', trigger='interval', minutes=10)
scheduler.add_job(userJob.crwalDetailJob, name='userJob.crwalDetailJob', trigger='interval', minutes=10)

#comments
scheduler.add_job(commentJob.crwalComment, name='commentJob.crwalComment', trigger='interval', minutes=10)
scheduler.add_job(commentJob.crwalNewComment, name='commentJob.crwalNewComment', trigger='interval', minutes=20)
scheduler.add_job(commentJob.crwalLatestComment, name='commentJob.crwalLatestComment', trigger='interval', hours=6)
scheduler.add_job(commentJob.crwalPastComment, name='commentJob.crwalPastComment', trigger='interval', days=14)

scheduler.start()

while True:
  time.sleep(2)
