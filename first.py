from spiders import article as articleSpider
from db import Session
from config import ARTICLE_SECTIONS

for section in ARTICLE_SECTIONS:
    articleSpider.crawlAndSave(section['type'], section['url'], 800, Session)