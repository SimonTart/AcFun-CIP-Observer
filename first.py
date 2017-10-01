from spiders import article as articleSpider
from config import ARTICLE_SECTIONS
from jobs.article import crawlNewArticleJob, crawlArticleDetailJob
from jobs import user as userJob

import logging
logging.basicConfig(level=logging.INFO)

# crawlNewArticleJob()

userJob.crwalBasicJob()