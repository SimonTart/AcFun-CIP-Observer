import requests
from db import Session
from models.comment import Comment
from time import time

def requestComments(articleId, pageNumber = 1, pageSize = 200):
    params = {
        'isNeedAllCount': 'true',
        'isReaderOnlyUpUser': 'false',
        'isAscOrder': 'false',
        'contentId': articleId,
        'currentPage': pageNumber,
        'pageSize': pageSize,
    }
    return requests.get('http://www.acfun.cn/comment_list_json.aspx', params=params)

def getCommentListFromRes(res):
    data = res.json().get('data')
    commentIdList = data.get('commentList')
    commentContentArr = data.get('commentContentArr')
    commentList = []
    for commentId in commentIdList:
        commentList.append(commentContentArr.get('c%d' % commentId))
    return commentList

def getCommentsByOrder(articleId, crawlAll):
    """根据文章ID抓取评论
    Args:
        articleId: 文章ID
        crawlAll: 是否抓取此文章的所有评论, 如果是False, 那么只抓取前200个

    Returns: commentList
    """
    res = requestComments(articleId)
    totalPage = res.json().get('data').get('totalPage')
    commentList = getCommentListFromRes(res)
    if crawlAll is True:
        for pageNumber in range(1, int(totalPage)):
            newComments = getCommentListFromRes(requestComments(articleId, pageNumber + 1))
            commentList.extend(newComments)
    return commentList
    

def formatCommentToModel(comment, articleId):
    return {
        'id': comment.get('cid'),
        'content': comment.get('content'),
        'userId': comment.get('userId'),
        'postDate': comment.get('postDate'),
        'quoteId': comment.get('quoteId'),
        'isDelete': comment.get('isDelete'),
        'isUpDelete': comment.get('isUpDelete'),
        'articleId': articleId,
    }

def fromatComments(comments, articleId):
    return [formatCommentToModel(comment, articleId) for comment in comments]

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
            'isDelete': c.get('isDelete'),
            'isUpDelete': c.get('isUpDelete')
        })
        session.commit()

    session.close()


def crawlCommentsByArticleId(articleId, crawlAll = False):
    comments = getCommentsByOrder(articleId, crawlAll)
    comments = fromatComments(comments, articleId)
    saveComments(comments)
    