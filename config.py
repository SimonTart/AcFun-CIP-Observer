import os

ARTICLE_SECTIONS = ({
  'type': '综合',
  'channelId': 110,
  'realmIds': '5,1,2,4',
},{
  'type': '工作·情感',
  'channelId': 73,
  'realmIds': '6,7',
},{
  'type': '动漫文化',
  'channelId': 74,
  'realmIds': '13,14',
},
{
  'type': '漫画·轻小说',
  'channelId': 75,
  'realmIds': '15,16',
},
{
  'type': '游戏',
  'channelId': 164,
  'realmIds': '8,10,11,9,12',
})

TYPE_TO_CHANNEL_ID = dict()
for section in ARTICLE_SECTIONS:
  TYPE_TO_CHANNEL_ID[section['type']] = section['channelId']

ARTICLE_UPDATE_PAGE_COUNT = 800
ARTICLE_CRAWL_PAGE_COUNT = 10
ARTICLE_CRAWL_DETAIL_PAST_DAY = 10

if os.getenv('PYTHON_ENV', 'development') == 'production':
  db = {
    'host': os.getenv('DB_HOST'),
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