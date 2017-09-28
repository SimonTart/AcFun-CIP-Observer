import requests
import re
import time
from bs4 import BeautifulSoup
from models.article import Article
from models.user import User
from db import Session
from config import TYPE_TO_CHANNEL_ID
from sqlalchemy import or_, update
import arrow

def crawl(type, baseUrl, pageNum):
  if pageNum == 1:
    index = ''
  else:
    index = '_' + str(pageNum)
  url = baseUrl.format(index)
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  articleTags = soup.select('#block-content-article .mainer .item')
  articles = set()
  for articleTag in articleTags:
    titleTag = articleTag.find('a', class_="title")
    idSearch = re.search(r'/a/ac(\d+)$', titleTag['href'], flags=re.I)
    if idSearch:
      id = idSearch.group(1)
    else:
      id = titleTag['href']
      yield None
      continue
    title = titleTag.string
    publishedAt = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', titleTag['title'], flags=re.I).group(0)
    hint = articleTag.find('a', class_="hint-comm-article")['title']
    commentNum = re.search(r'共有(\d+)条评论', hint).group(1)
    viewNum = re.search(r'(\d+)人围观', hint).group(1)
    publishedBy = re.search(r'uid=(\d+)', articleTag.find('a', class_="name")['href']).group(1)
    yield {
      'id': id,
      'type': type,
      'title': title,
      'commentNum': commentNum,
      'viewNum': viewNum,
      'publishedAt': publishedAt,
      'publishedBy': publishedBy
    }


def crawlAndSave(type, baseUrl, pageCount):
  count = 0
  new = 0
  update = 0
  for page in range(1, pageCount):
    time.sleep(10)
    session = Session()
    for article in crawl(type, baseUrl, page):
      if article == None:
        continue
      existArticle = session.query(Article).filter_by(id = article['id']).first()
      count += 1
      user = session.query(User).filter_by(id = article['publishedBy']).first()
      if user == None:
        session.add(User(id=article['publishedBy']))
        session.commit()
      if existArticle:
        session.query(Article).filter_by(id = article['id']).update(article)
        update += 1
      else:
        session.add(Article(**article))
        new += 1
    session.commit()
    session.close()
  return count, new, update

def crawlArticleDetail(id, type):
  params = { 'contentId': id, 'channelId': TYPE_TO_CHANNEL_ID[type] }
  result = requests.get('http://www.acfun.cn/content_view.aspx', params=params).json();
  return {
    'viewNum': result[0],
    'commentNum': result[1],
    'bananaNum': result[6]
  }


def crawlDetailAndSave(pastDay):
  session = Session()
  articles = session.query(
    Article.id,
    Article.type,
    Article.bananaNum,
  ).filter(Article.publishedAt >= arrow.now().shift(days=-pastDay).format('YYYY-MM-DD')).all()
  session.close()
  for article in articles:
    time.sleep(10)
    session = Session()
    detail = crawlArticleDetail(article.id, article.type)
    session.query(Article).filter_by(id = article.id).update(detail)
    session.commit()
    session.close()
  return len(articles)

def completeDetailAndSave():
  session = Session()
  articles = session.query(
    Article.id,
    Article.type,
    Article.bananaNum,
  ).filter(Article.bananaNum == None).limit(100).all()
  session.close()
  for article in articles:
    time.sleep(3)
    session = Session()
    detail = crawlArticleDetail(article.id, article.type)
    session.query(Article).filter_by(id = article.id).update(detail)
    session.commit()
    session.close()
  return len(articles)
  
