from spiders import article as ArticleSpider
from config import ARTICLE_SECTIONS, ARTICLE_UPDATE_PAGE_COUNT, ARTICLE_CRAWL_PAGE_COUNT, ARTICLE_CRAWL_DETAIL_PAST_DAY
from common.utils import recordJobCoastTime
import time
import logging

def articleJob(jobName, sections, pageCount):
  totalCount = 0
  totalNew = 0
  totalUpdate = 0
  logger = logging.getLogger(jobName)
  for section in sections:
    count, new, update = ArticleSpider.crawlAndSave(section['type'], section['url'], pageCount)
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

def crawlArticleDetailJob(jobName, pastDay):
  count = ArticleSpider.crawlDetailAndSave(pastDay=pastDay)
  logger = logging.getLogger(jobName)
  logger.info('[Article]: crawl %(count)d articles detail', {
    'count': count,
  })

crawlNewArticleJob = recordJobCoastTime(articleJob, 'crawlNewArticleJob', sections=ARTICLE_SECTIONS, pageCount=ARTICLE_CRAWL_PAGE_COUNT)
crawlArticleDetailJob = recordJobCoastTime(crawlArticleDetailJob, 'crawlArticleDetailJob', pastDay=ARTICLE_CRAWL_DETAIL_PAST_DAY)
