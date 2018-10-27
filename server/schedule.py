import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from config import ARTICLE_SECTIONS as articleSections, VIDEO_SECTIONS as videoSections
from .spiders.content import ContentSpider
import server.spiders.comment as commentSpider
from sentry import ravenClient
from .models.spiderRecord import SpiderRecord
from db import Session
import arrow
from config import contentTypes

CRAWL_LATEST_COMMENT = 'CRAWL_LATEST_COMMENT'

scheduler = BlockingScheduler()


# 抓取最新的文章
# scheduler.add_job(contentSpider.crawlAllSectionsArticles, args= [articleSections], name='抓取最新文章', trigger='interval', minutes=10)

# 抓取最新的视频
# scheduler.add_job(contentSpider.crawlAllSectionsVideos, args= [videoSections], name='抓取最新视频', trigger='interval', minutes=10)

## 最近一天的文章的评论，每15分钟抓取最近三天的评论
# scheduler.add_job(commentSpider.crawlLatestComments, args= [3], name='抓取一天内最新评论', trigger='interval', minutes=5)

## 每小时抓一次最近三天的评论
# scheduler.add_job(commentSpider.crawlLatestComments, args= [3], name='抓取三天内最新评论', trigger='interval', hours=1)

## 最近一周的评论 每晚抓取一次评论
# scheduler.add_job(commentSpider.crawlLatestComments, kwargs= { 'day': 7, 'useThread': False, 'crawlAll': True}, name='抓取一周内文章评论', trigger='cron', hour=5, minute=30)

def errorListener(event):
    ravenClient.capture(event.exception)

scheduler.add_listener(errorListener, mask = apscheduler.events.EVENT_JOB_ERROR)
