import requests
import logging
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
  