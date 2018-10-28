import apscheduler
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from config import ARTICLE_SECTIONS, VIDEO_SECTIONS, contentTypes
from .spiders.content import ContentSpider
from .spiders.comment import crawl_content_latest_comments
from sentry import ravenClient
from config import contentTypes

scheduler = BlockingScheduler()


# 抓取内容的最新评论
def crawl_section_content_latest_comment(sections, content_type):
    for section in sections:
        if 'subSections' not in section:
            crawl_content_latest_comments(section, content_type)
        else:
            for sub_section in section['subSections']:
                crawl_content_latest_comments(sub_section, content_type)

def crawl_section_content_latest_comment_thread(sections, content_type):
    thread_list = []
    for section in sections:
        if 'subSections' not in section:
            t = threading.Thread(target=crawl_content_latest_comments, args=(section, content_type))
            t.start()
            thread_list.append(t)
        else:
            for sub_section in section['subSections']:
                t = threading.Thread(target=crawl_content_latest_comments, args=(sub_section, content_type))
                t.start()
                thread_list.append(t)

    return thread_list

#抓取所有内容的最新评论
def crawl_all_content_latest_comment():
    crawl_section_content_latest_comment(ARTICLE_SECTIONS, contentTypes['article'])
    crawl_section_content_latest_comment(VIDEO_SECTIONS, contentTypes['video'])

def crawl_all_content_latest_comment_thread():
    thread_list = []
    article_thread_list = crawl_section_content_latest_comment_thread(ARTICLE_SECTIONS, contentTypes['article'])
    video_thread_list = crawl_section_content_latest_comment_thread(VIDEO_SECTIONS, contentTypes['video'])
    thread_list.extend(article_thread_list)
    thread_list.extend(video_thread_list)

    for thread in thread_list:
        thread.join()


def errorListener(event):
    ravenClient.capture(event.exception)


scheduler.add_job(crawl_all_content_latest_comment, name='抓取所有内容的最新评论', trigger='interval', minutes=1, max_instances=1)



scheduler.add_listener(errorListener, mask = apscheduler.events.EVENT_JOB_ERROR)
