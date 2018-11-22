import log
import traceback
from server.spiders.content import crawl_all_sections_articles, crawl_all_sections_videos
from server.spiders.comment import crawl_content_latest_comments, CommentSpider
from server.schedule import crawl_all_content_latest_comment, crawl_all_content_latest_comment_thread
from time import time
from server import server
from config import ARTICLE_SECTIONS, VIDEO_SECTIONS, contentTypes


# 获取最近10页的内容
# crawl_all_sections_articles(ARTICLE_SECTIONS, total_page=10)
# crawl_all_sections_videos(VIDEO_SECTIONS, total_page=10)

# 获取这个之前的内容
# crawl_all_sections_videos(VIDEO_SECTIONS, min_published_date='2018-11-17 00:00:00')
# crawl_all_sections_articles(ARTICLE_SECTIONS, min_published_date='2018-11-17 00:00:00')

# 获取新动态的文章
# crawl_all_sections_articles(ARTICLE_SECTIONS, article_order_type=1, is_get_latest_comment=True)

# 获取content所有的评论
# CommentSpider(content_id=4667805, crawl_all=True).crawl_comments()

# 抓取时间范围内的评论
# CommentSpider(content_id=4667805, min_comment_time='2018-10-26 12:00:00').crawl_comments()

# 抓取文章中没抓取的评论
# crawl_content_latest_comments(ARTICLE_SECTIONS[0], contentTypes['article'])

# 抓取视频中没抓取的评论
# crawl_content_latest_comments(VIDEO_SECTIONS[1], contentTypes['video'])

#schedul 抓取所有的最近评论
# crawl_all_content_latest_comment()
crawl_all_content_latest_comment_thread()

