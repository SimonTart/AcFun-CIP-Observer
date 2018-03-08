import requests
from .utils import formatTimestamp
from ..model.article import Article
from db import Session

def getArticlesByOrder(realmIds, pageNumber = 1, pageSize = 200):
    params = {
        'pageNo': pageNumber,
        'size': pageSize,
        'realmIds': realmIds,
        'originalOnly': 'false',
        'orderType': 2,
        'periodType': -1,
        'filterTitleImage': 'true',
        '1': 2
    }
    res = requests.get("http://webapi.aixifan.com/query/article/list", params=params)
    return res.json().get('data').get('articleList')


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
    newArticles = []
    for article in articles:
        newArticles.append(formatArticleToModle(article))
    return newArticles

def saveArticles(articles):
    session = Session()
    for article in articles:
        exist = session.query(Article).filter_by(id = article['id']).first()
        if exist is not None:
            session.query(Article).filter_by(id = article['id']).update(article)
        else:
            session.add(Article(**article))
        session.commit()
    session.close()
            
        # if exist


def startSpider(section):
    articleList = getArticlesByOrder(section.get('realmIds'), pageSize=20)
    articleList = formatArticles(articleList)
    saveArticles(articleList)


        