import server.spiders.article as articleSpider
import server.spiders.comment as commentSpider
from server.schedule import scheduler
from time import time
from server import server
from config import ARTICLE_SECTIONS

if __name__ == '__main__':
  scheduler.start()
  server.run(host='127.0.0.1', port=8000)
# start = time()
# articleSpider.crawlAllSectionsArticles(ARTICLE_SECTIONS)
# print('cost', time() - start)

# commentSpider.crawlLatestComments(1, useThread=False, crawlAll=True)
