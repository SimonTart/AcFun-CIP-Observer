import requests
from .utils import formatTimestamp
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


def saveArticles(section):
    articleList = getArticlesByOrder(section.get('realmIds'), pageSize=20)
    for article in articleList:
        print(formatTimestamp(article.get('contribute_time')))


        