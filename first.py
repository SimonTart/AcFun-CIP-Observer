from main import articleJob
from config import ARTICLE_SECTIONS

for section in ARTICLE_SECTIONS:
    ArticleSpider.crawlAndSave(section['type'], section['url'], 800, Session)