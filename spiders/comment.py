import requests
import logging
import time

from db import Session
from models.content import Content
from models.user import User
from models.comment import Comment

def getTotalPage(id):
  try:
    params = { 'contentId': id, 'currentPage': 1}
    result = requests.get('http://www.acfun.cn/comment_list_json.aspx', params=params).json()
  except Exception as error:
    logging.error(error)
  else:
    if result.get('success') != True or result.get('status') != 200:
      logging.error(result.get('msg'))
      raise RuntimeError('Can\'t get comments totalPage')
    else:
      return int(result.get('data').get('totalPage'))

def saveUserIds(userIds):
  session = Session()
  existUserIds = session.query(User.id).filter(User.id.in_(userIds)).all()
  newUsers = map(lambda id: User(id=id), set(id for id in userIds if id >= 0) - set(u.id for u in existUserIds))
  session.add_all(list(newUsers))
  session.commit()
  session.close()

def saveComments(comments, contentId):
  commentIds = list(map(lambda c: int(c.get('cid')), list(comments)))
  session = Session()
  existCommentIds = [c.id for c in session.query(Comment.id).filter(Comment.id.in_(commentIds)).all()]
  updatedComments = map(lambda c: {
    'id': c.get('cid'),
    'isDelete': c.get('isDelete'),
    'isUpDelete': c.get('isUpDelete')
  },filter(lambda c: c.get('cid') in existCommentIds,comments))
  for comment in updatedComments:
    session.query(Comment).filter(Comment.id == comment.get('id')).update(comment)
  newCommentId = set(commentIds) - set(existCommentIds)
  newComments = map(
    lambda c: Comment(
      id=int(c.get('cid')),
      content=c.get('content'),
      userId=int(c.get('userID')),
      postDate=c.get('postDate'),
      quoteId=int(c.get('quoteId')),
      isDelete=c.get('isDelete'),
      isUpDelete=c.get('isUpDelete'),
      contentId=contentId
    ),
    [c for c in comments if c.get('cid') in newCommentId]
  )
  session.add_all(list(newComments))
  session.commit()
  session.close()

def crawl(id, sleep = 1):
  for page in range(1, getTotalPage(id) + 1):
    try:
      params = { 'contentId': id, 'currentPage': page}
      result = requests.get('http://www.acfun.cn/comment_list_json.aspx', params=params).json()
      commentContentArr = result.get('data').get('commentContentArr')
      userIds = set(map(lambda c: int(c.get('userID')) ,commentContentArr.values()))
      saveUserIds(userIds)
      saveComments(commentContentArr.values(), id)
      time.sleep(sleep)
    except Exception as error:
      logging.error(error)
  session = Session()
  session.query(Content).filter(Content.id == id).update({ 'crawlComments': True })
  session.commit()
  session.close()