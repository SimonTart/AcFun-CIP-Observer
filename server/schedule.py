from apscheduler.schedulers.background import BackgroundScheduler
from config import ARTICLE_SECTIONS as sections
import server.spiders.article as articleSpider

scheduler = BackgroundScheduler()

scheduler.add_job(articleSpider.crawlAllSectionsArticles, args= [sections], trigger='interval', minutes=1)

