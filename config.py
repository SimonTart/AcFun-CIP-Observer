import os

ARTICLE_SECTIONS = ({
  'type': '综合',
  'url': 'http://www.acfun.cn/v/list110/index{0}.htm',
},{
  'type': '工作·情感',
  'url': 'http://www.acfun.cn/v/list73/index{0}.htm'
},{
  'type': '动漫文化',
  'url': 'http://www.acfun.cn/v/list74/index{0}.htm'
},
{
  'type': '漫画·轻小说',
  'url': 'http://www.acfun.cn/v/list75/index{0}.htm'
},
{
  'type': '游戏',
  'url': 'http://www.acfun.cn/v/list164/index{0}.htm'
})

ARTICLE_UPDATE_PAGE_COUNT = 800
ARTICLE_CRAWL_PAGE_COUNT = 10

if os.getenv('PYTHON_ENV', 'development') == 'production':
  db = {
    'host': 'DB_HOST',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSPORT'),
    'database': os.getenv('DB_NAME')
  }
else:
  db = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'eva_acfun_dev'
  }