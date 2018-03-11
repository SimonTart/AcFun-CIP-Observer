import requests
import threading
from time import time
from .utils import formatTimestamp
from ..models.article import Article
from db import Session

def getOnePageArticles(realmIds, pageNumber = 1, pageSize = 20):
    params = {
        'pageNo': pageNumber,
        'size': pageSize,
        'realmIds': realmIds,
        'originalOnly': 'false',
        'orderType': 2,
        'periodType': -1,
        'filterTitleImage': 'true',
    }
    res = requests.get("http://webapi.aixifan.com/query/article/list", params=params)
    return res.json().get('data').get('articleList')

def getArticles(realmIds, totalPage):
    articleList = []
    for pageNumber in range(1, totalPage + 1):
        articleList.extend(getOnePageArticles(realmIds, pageNumber))
    return articleList


def formatArticleToModle(article):
    return {
        'id': article.get('id'),
        'type': article.get('channel_name'),
        'title': article.get('title'),
        'viewNum': article.get('view_count'),
        'commentNum': article.get('comment_count'),
        'realmId': article.get('realm_id'),
        'realmName': article.get('realm_name'),
        'publishedAt': formatTimestamp(article.get('contribute_time')),
        'publishedBy': article.get('user_id'),
        'bananaNum': article.get('banana_count')
    }

def formatArticles(articles):
    return [formatArticleToModle(article) for article in articles]

def saveArticles(articles):
    session = Session()
    articleIds = { article['id'] for article in articles }
    articlesInDB = session.query(Article.id).filter(Article.id.in_(articleIds)).all()
    articleIdsInDB = { article.id for article in articlesInDB }

    needToSaveArticleIds = articleIds - articleIdsInDB
    needToSabeArticles = list(filter(lambda a: a['id'] in needToSaveArticleIds, articles))
    session.add_all([ Article(**article) for article in needToSabeArticles])
    session.commit()

    session.close()


def crawlArticlesBySection(section, totalPage = 1):
    start  = time()
    startGetTime = time()

    articleList = getArticles(section.get('realmIds'), totalPage)
    timeOfGet = time() - startGetTime

    startSaveTime = time()
    articleList = formatArticles(articleList)
    saveArticles(articleList)
    timeOfSave = time() - startSaveTime

    timeOfTotal = time() - start
    print(
        '抓取', section.get('type'), '区文章：',
        '[一共花费', timeOfTotal, ' 秒]',
        '[请求数据花费', timeOfGet,'秒]',
        '[处理并保存数据花费', timeOfSave,'秒]',
        )

def crawlAllSectionsArticles(sections):
    threadList = []
    start = time()
    for section in sections:
        t = threading.Thread(target = crawlArticlesBySection, args=(section,))
        t.start()
        threadList.append(t)
    
    for t in threadList:
        t.join()
    print('此次抓取文章共使用：', time() - start, '秒')
        
