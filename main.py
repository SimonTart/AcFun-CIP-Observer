from spiders import article as ArticleSpider
from config import ARTICLE_SECTIONS, ARTICLE_PAGE_COUNT
from db import Session
import schedule
import time


def articleJob():
  for section in ARTICLE_SECTIONS:
    ArticleSpider.crawlAndSave(section['type'], section['url'], ARTICLE_PAGE_COUNT, Session)


schedule.every(10).minutes.do(articleJob)

while True:
    schedule.run_pending()
    time.sleep(10 * 100)