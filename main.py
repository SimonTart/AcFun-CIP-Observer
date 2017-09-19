from spiders import article as ArticleSpider
from config import ARTICLE_SECTIONS, ARTICLE_UPDATE_PAGE_COUNT, ARTICLE_CRAWL_PAGE_COUNT
from apscheduler.schedulers.background import BackgroundScheduler
from db import Session
from utils import recordJobCoastTime
import time


scheduler = BackgroundScheduler()



def crawlNewArticleJob():
  for section in ARTICLE_SECTIONS:
    ArticleSpider.crawlAndSave(section['type'], section['url'], ARTICLE_CRAWL_PAGE_COUNT, Session)

def updateArticleJob(sections, pageCount, Session):
  for section in sections:
    total, new, old = ArticleSpider.crawlAndSave(section['type'], section['url'], pageCount, Session)
    print
updateArticles = recordJobCoastTime(updateArticleJob, 'updateArticleJob', sections=ARTICLE_SECTIONS, pageCount=ARTICLE_UPDATE_PAGE_COUNT , Session=Session)


def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

# scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.add_job(updateArticles, 'interval', minutes=1)
scheduler.start()

# This is here to simulate application activity (which keeps the main thread alive).
while True:
  time.sleep(2)
