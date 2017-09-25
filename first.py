from spiders import article as articleSpider
from config import ARTICLE_SECTIONS

import logging
logging.basicConfig(level=logging.INFO)

for section in ARTICLE_SECTIONS:
    articleSpider.crawlAndSave(section['type'], section['url'], 100)