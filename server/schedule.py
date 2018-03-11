from apscheduler.schedulers.background import BackgroundScheduler
from config import ARTICLE_SECTIONS as articleSections, VIDEO_SECTIONS as videoSections
import server.spiders.content as contentSpider
import server.spiders.comment as commentSpider

scheduler = BackgroundScheduler()

# 抓取最新的文章
scheduler.add_job(contentSpider.crawlAllSectionsArticles, args= [articleSections], name='抓取最新文章', trigger='interval', minutes=5)

# 抓取最新的视频
scheduler.add_job(contentSpider.crawlAllSectionsVideos, args= [videoSections], name='抓取最新视频', trigger='interval', minutes=5)

## 最近三天的文章的评论，每分钟抓取一次每篇文章最近的50条
scheduler.add_job(commentSpider.crawlLatestComments, args= [3], name='抓取三天内文章最新评论', trigger='interval', minutes=1)

## 最近一周的评论 每晚抓取一次每篇文章的所有评论
scheduler.add_job(commentSpider.crawlLatestComments, kwargs= { 'day': 7, 'useThread': False, 'crawlAll': True}, name='抓取一周内文章评论', trigger='cron', hour=5, minute=30)
