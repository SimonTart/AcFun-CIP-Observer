from spiders import article as articleSpider
from config import ARTICLE_SECTIONS
from jobs.article import crawlNewArticleJob, crawlArticleDetailJob

import logging
logging.basicConfig(level=logging.INFO)

crawlNewArticleJob()