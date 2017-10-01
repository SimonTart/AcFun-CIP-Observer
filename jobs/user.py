import time
from sqlalchemy import and_

from db import Session
from models.user import User
from spiders import user as userSpider

def crwalBasicJob():
  session = Session()
  users = session.query(User.id).filter(and_(
    User.name == None,
    User.disabled != True
  )).limit(100).all()
  session.close()
  for user in users:
    userSpider.crawlBasic(user.id)
    time.sleep(5)

def crwalDetailJob():
  session = Session()
  users = session.query(User.id).filter(and_(
    User.postNum == None,
  )).limit(100).all()
  session.close()
  for user in users:
    userSpider.crawlDetail(user.id)
    time.sleep(5)
