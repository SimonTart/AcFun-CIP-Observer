from spiders import article as ArticleSpider
from config import ARTICLE_SECTIONS, ARTICLE_UPDATE_PAGE_COUNT, ARTICLE_CRAWL_PAGE_COUNT
from db import Session
from common.utils import recordJobCoastTime
import time
import logging

def articleJob(jobName, sections, pageCount, Session):
  print('Article Job')
  totalCount = 0
  totalNew = 0
  totalUpdate = 0
  logger = logging.getLogger(jobName)
  for section in sections:
    count, new, update = ArticleSpider.crawlAndSave(section['type'], section['url'], pageCount, Session)
    logger.info('[Article %(type)s]: crawl %(count)d articles, %(new)d create, %(update)d update', {
      'type': section['type'],
      'count': count,
      'new': new,
      'update': update
    })
    totalCount += count
    totalNew += new
    totalUpdate += update
  logger.info('[Article]: crawl %(count)d articles, %(new)d create, %(update)d update', {
    'count': totalCount,
    'new': totalNew,
    'update': totalUpdate
  })

updateArticleJob = recordJobCoastTime(articleJob, 'updateArticleJob', sections=ARTICLE_SECTIONS, pageCount=ARTICLE_UPDATE_PAGE_COUNT , Session=Session)
crawlNewArticleJob = recordJobCoastTime(articleJob, 'crawlNewArticleJob', sections=ARTICLE_SECTIONS, pageCount=ARTICLE_CRAWL_PAGE_COUNT , Session=Session)
