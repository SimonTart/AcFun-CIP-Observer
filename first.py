from spiders import article as articleSpider
from config import ARTICLE_SECTIONS
from jobs.article import crawlNewArticleJob, crawlArticleDetailJob
from jobs import user as userJob, comment as commentJob

import logging
logging.basicConfig(level=logging.INFO)

commentJob.crwalNewComment()
# crawlNewArticleJob()

# userJob.crwalBasicJob()
# userJob.crwalDetailJob()