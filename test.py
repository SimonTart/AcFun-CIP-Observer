import logging
import traceback
from server.spiders.content import ContentSpider
import server.spiders.comment as commentSpider
from server.schedule import scheduler
from time import time
from server import server
from config import ARTICLE_SECTIONS, VIDEO_SECTIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

# if __name__ == '__main__':
#   scheduler.start()
  # server.run(host='127.0.0.1', port=8000)
# start = time()
# print('cost', time() - start)

# contentSpider.crawlAllSectionsArticles(ARTICLE_SECTIONS, totalPage = 1)
# contentSpider.crawlAllSectionsVideos(VIDEO_SECTIONS, totalPage = 1)
# commentSpider.crawlLatestComments(1, useThread=True, crawlAll=False)
# commentSpider.crawlCommentsByContentId(4259705, True)

ContentSpider().crawl_all_sections_articles(ARTICLE_SECTIONS, total_page=10)
ContentSpider().crawl_all_sections_videos(VIDEO_SECTIONS, total_page=10)
