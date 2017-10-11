import time
from sqlalchemy import and_
import arrow

from spiders import comment as commentSpider
from db import Session
from models.article import Article 

def crwalComment():
  session = Session()
  articles = session.query(Article.id).filter(Article.crawlComments == False).limit(100).all()
  session.close()
  for article in articles:
    commentSpider.crawl(article.id, sleep = 0.1)

# 过去最近的文章
def crwalNewComment():
  session = Session()
  articles = session.query(Article.id).filter(Article.publishedAt >= arrow.now().shift(days=-1).format('YYYY-MM-DD HH:MM:SS')).all()
  session.close()
  for article in articles:
    commentSpider.crawl(article.id, sleep = 0.1)

# 过去两天的文章
def crwalLatestComment():
  session = Session()
  articles = session.query(Article.id).filter(Article.publishedAt >= arrow.now().shift(days=-3).format('YYYY-MM-DD HH:MM:SS')).all()
  session.close()
  for article in articles:
    commentSpider.crawl(article.id)

# 过去14天的文章
def crwalPastComment():
  session = Session()
  articles = session.query(Article.id).filter(Article.publishedAt >= arrow.now().shift(days=-14).format('YYYY-MM-DD')).all()
  session.close()
  for article in articles:
    commentSpider.crawl(article.id)