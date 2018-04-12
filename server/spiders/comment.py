import logging
import requests
import threading
import arrow
from db import Session
from ..models.comment import Comment
from ..models.content import Content
from time import time
from sentry import ravenClient

def requestComments(contentId, pageNumber = 1, pageSize = 50):
    params = {
        'isNeedAllCount': 'true',
        'isReaderOnlyUpUser': 'false',
        'isAscOrder': 'false',
        'contentId': contentId,
        'currentPage': pageNumber,
        'pageSize': pageSize,
    }
    return requests.get('http://www.acfun.cn/comment_list_json.aspx', params=params)

def getCommentDictFromRes(res):
    data = res.json().get('data')
    commentIdList = data.get('commentList')
    return data.get('commentContentArr')

def getCommentsByOrder(contentId, crawlAll):
    """根据content ID抓取评论
    Args:
        contentId: content ID
        crawlAll: 是否抓取此内容的所有评论, 如果是False, 那么只抓取前200个

    Returns: commentList
    """
    res = requestComments(contentId)
    totalPage = res.json().get('data').get('totalPage')
    commentDict = getCommentDictFromRes(res)
    if crawlAll is True:
        for pageNumber in range(1, int(totalPage)):
            newCommentDict = getCommentDictFromRes(requestComments(contentId, pageNumber + 1))
            commentDict.update(newCommentDict)

    return commentDict.values()
    

def formatCommentToModel(comment, contentId):
    return {
        'id': comment.get('cid'),
        'content': comment.get('content'),
        'userId': comment.get('userID'),
        'postDate': comment.get('postDate'),
        'quoteId': comment.get('quoteId'),
        'isDelete': comment.get('isDelete'),
        'isUpDelete': comment.get('isUpDelete'),
        'contentId': contentId,
    }

def fromatComments(comments, contentId):
    return [formatCommentToModel(comment, contentId) for comment in comments]

def saveComments(comments):
    session = Session()
    commentIds = { comment['id'] for comment in comments }
    commentsInDB = session.query(Comment.id).filter(Comment.id.in_(commentIds)).all()
    commentIdsInDB = { comment.id for comment in commentsInDB }
    if commentIdsInDB is None:
        commentIdsInDB = []
    commentIdsInDB = set(commentIdsInDB)

    # 添加新的评论
    needAddCommentIds = commentIds - commentIdsInDB
    needAddComments = list(filter(lambda c: c['id'] in needAddCommentIds, comments))
    session.add_all([ Comment(**comment) for comment in needAddComments])
    session.commit()

    #更新旧的评论
    needUpdateComments = list(filter(lambda c: c['id'] in commentIdsInDB and (c['isDelete'] is True or c['isUpDelete'] is True), comments))
    for comment in needUpdateComments:
        session.query(Comment).filter(Comment.id == comment.get('id')).update({
            'isDelete': comment.get('isDelete'),
            'isUpDelete': comment.get('isUpDelete')
        })
        session.commit()

    session.close()


def crawlCommentsByContentId(contentId, crawlAll):
    try:
        start  = time()
        startGetTime = time()

        comments = getCommentsByOrder(contentId, crawlAll)
        timeOfGet = time() - startGetTime

        startSaveTime = time()
        comments = fromatComments(comments, contentId)
        saveComments(comments)
        timeOfSave = time() - startSaveTime

        timeOfTotal = time() - start
        # print(
        #     '抓取内容：', contentId, '评论'
        #     '[一共花费', timeOfTotal, ' 秒]',
        #     '[请求数据花费', timeOfGet,'秒]',
        #     '[处理并保存数据花费', timeOfSave,'秒]',
        #     )
    except: 
        ravenClient.captureException()

def crawlCommentsByContentIds(contentIds, crawlAll):
    for contentId in contentIds:
        crawlCommentsByContentId(contentId, crawlAll)
    
def crawlLatestComments(day, useThread = True, threadCrawlNum = 100, crawlAll = False):
    start = time()
    session = Session()
    contents = session.query(Content.id).filter(Content.publishedAt >= arrow.now().shift(days= -day).format('YYYY-MM-DD HH:MM:SS')).all()
    contentIds = [ c.id for c in contents ]
    if useThread:
        threadList = []
        for i in range(0, len(contentIds) + 1, threadCrawlNum):
            t = threading.Thread(target = crawlCommentsByContentIds, args = (contentIds[i:i+threadCrawlNum], crawlAll))
            t.start()
            threadList.append(t)

        for t in threadList:
            t.join()
    else:
        crawlCommentsByContentIds(contentIds, crawlAll)
    logging.info('此次一共抓取' + str(len(contentIds)) + '个内容的评论，共使用：' + str(time() - start) + '秒')
    