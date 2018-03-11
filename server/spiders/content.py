import requests
import threading
from time import time
from .utils import formatTimestamp
from ..models.content import Content
from db import Session
from config import contentTypes

def getOnePageContents(section, sectionType, pageNumber = 1, pageSize = 100):
    if sectionType == contentTypes['article']:
        params = {
            'pageNo': pageNumber,
            'size': pageSize,
            'realmIds': section.get('realmIds'),
            'originalOnly': 'false',
            'orderType': 2,
            'periodType': -1,
            'filterTitleImage': 'true',
        }
        res = requests.get("http://webapi.aixifan.com/query/article/list", params=params)
        return res.json().get('data').get('articleList')

def getContents(section, sectionType, totalPage):
    contentList = []
    for pageNumber in range(1, totalPage + 1):
        contentList.extend(getOnePageContents(section, sectionType, pageNumber))
    return contentList


def formatContentToModle(content, sectionType):
    if sectionType == contentTypes['article']:
        return {
            'id': content.get('id'),
            'type': content.get('channel_name'),
            'title': content.get('title'),
            'viewNum': content.get('view_count'),
            'commentNum': content.get('comment_count'),
            'realmId': content.get('realm_id'),
            'realmName': content.get('realm_name'),
            'publishedAt': formatTimestamp(content.get('contribute_time')),
            'publishedBy': content.get('user_id'),
            'bananaNum': content.get('banana_count'),
            'contentType': sectionType
        }

def formatContents(contents, sectionType):
    return [formatContentToModle(content, sectionType) for content in contents]

def saveContents(contents):
    session = Session()
    contentIds = { content['id'] for content in contents }
    contentsInDB = session.query(Content.id).filter(Content.id.in_(contentIds)).all()
    contentIdsInDB = { content.id for content in contentsInDB }

    needToSaveContentIds = contentIds - contentIdsInDB
    needToSabeContents = list(filter(lambda a: a['id'] in needToSaveContentIds, contents))
    session.add_all([ Content(**content) for content in needToSabeContents])
    session.commit()

    session.close()


def crawlContentsBySection(section, sectionType, totalPage = 1):
    start  = time()
    startGetTime = time()

    contentList = getContents(section, sectionType, totalPage)
    timeOfGet = time() - startGetTime

    startSaveTime = time()
    contentList = formatContents(contentList, sectionType)
    saveContents(contentList)
    timeOfSave = time() - startSaveTime

    timeOfTotal = time() - start
    print(
        '抓取[', section.get('name'), ']分区内容',
        '[一共花费', timeOfTotal, ' 秒]',
        '[请求数据花费', timeOfGet,'秒]',
        '[处理并保存数据花费', timeOfSave,'秒]',
        )

def crawlAllSectionsArticles(sections):
    threadList = []
    start = time()
    for section in sections:
        t = threading.Thread(target = crawlContentsBySection, args=(section, contentTypes['article']))
        t.start()
        threadList.append(t)
    
    for t in threadList:
        t.join()
    print('此次抓取文章共使用：', time() - start, '秒')
        
