import requests
import logging
from bs4 import BeautifulSoup

from models.user import User
from db import Session

def crawlBasic(id):
  try:
    result = requests.get('http://www.acfun.cn/usercard.aspx?uid=' + str(id)).json()
  except Exception as error:
    logging.error(error)
  else:
    if result['success'] == False and result['info'] == '用户被封禁':
      user = { 'disabled': True }
    else:
      userjson = result['userjson']
      user = {
        'gender' : userjson.get('gender'),
        'sign' : userjson.get('sign'),
        'avatar': userjson.get('avatar'),
        'lastLoginIp': userjson.get('lastLoginIp'),
        'registerAt': userjson.get('regTime'),
        'name': userjson.get('name'),
        'comeFrom': userjson.get('comeFrom')
      }
    session = Session();
    session.query(User).filter_by(id = id).update(user)
    session.commit()
    session.close()

def crawlDetail(id):
  try:
    result = requests.get('http://www.acfun.cn/u/{0}.aspx'.format(id))
  except Exception as error:
    logging.error(error)
  else:
    if result.status_code == 404:
      return
    soup = BeautifulSoup(result.text, 'html.parser')
    # print(int(soup.select('.contentlist .table [data-con="0"] span'))
    user = {
      'postNum': int(soup.select('.information .sub')[0].string),
      'followNum': int(soup.select('.information .follow')[0].string),
      'fansNum': int(soup.select('.information .fans')[0].string),
      'postVideoNum': int(soup.select('.contentlist .table [data-con="0"] span')[0].string),
      'postArticleNum': int(soup.select('.contentlist .table [data-con="1"] span')[0].string)
    }
    session = Session();
    session.query(User).filter_by(id = id).update(user)
    session.commit()
    session.close()
  