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

# 获取最近10页的内容
# ContentSpider(total_page=10).crawl_all_sections_articles(ARTICLE_SECTIONS)
# ContentSpider(total_page=10).crawl_all_sections_videos(VIDEO_SECTIONS)

# 获取这个之前的内容
# ContentSpider(min_published_date='2018-10-26 00:00:00').crawl_all_sections_videos(VIDEO_SECTIONS)
# ContentSpider(min_published_date='2018-10-26 00:00:00').crawl_all_sections_articles(ARTICLE_SECTIONS)

# 获取新评论的文章
ContentSpider(article_order_type=1, min_latest_comment_time='2018-10-26 00:00:00').crawl_all_sections_articles(ARTICLE_SECTIONS)




