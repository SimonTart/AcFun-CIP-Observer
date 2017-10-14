from spiders import article as articleSpider
from config import ARTICLE_SECTIONS
from jobs.article import crawlNewArticleJob, crawlArticleDetailJob
from jobs import user as userJob, comment as commentJob
from server.app import comment

import logging
logging.basicConfig(level=logging.INFO)

# commentJob.crwalNewComment()
# crawlNewArticleJob()

# userJob.crwalBasicJob()
# userJob.crwalDetailJob()