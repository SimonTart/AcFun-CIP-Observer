import logging
import sys
from ..proxy import Proxy
import threading
from time import time
from .utils import formatTimestamp
from ..models.content import Content
from db import Session
from config import contentTypes
from sentry import ravenClient
import arrow


class ContentSpider:
    def __init__(
        self,
        section,
        section_type,
        total_page=100,
        page_size=100,
        article_order_type=2,
        min_published_date=None,
        min_latest_comment_time=None
    ):
        """
        :param section:
        :param section_type:
        :param total_page:
        :param page_size:
        :param article_order_type: 1 是最新动态 2 是最新发表
        :param min_published_date:
        :param min_latest_comment_time:
        """
        self.section = section
        self.section_type = section_type
        self.total_page = total_page
        self.page_size = page_size
        self.article_order_type = article_order_type
        self.min_published_date = min_published_date
        self.min_latest_comment_time = min_latest_comment_time

    def format_content_to_model(self, content):
        if self.section_type == contentTypes['article']:
            return {
                'id': content.get('id'),
                'type': content.get('channel_name'),
                'title': content.get('title'),
                'viewNum': content.get('view_count'),
                'commentNum': content.get('comment_count'),
                'realmId': content.get('realm_id'),
                'realmName': content.get('realm_name'),
                'latestCommentTime': formatTimestamp(content.get('latest_comment_time')),
                'publishedAt': formatTimestamp(content.get('contribute_time')),
                'publishedBy': content.get('user_id'),
                'bananaNum': content.get('banana_count'),
                'contentType': self.section_type,
                'channelId': self.section['channelId']
            }

        if self.section_type == contentTypes['video']:
            return {
                'id': content.get('id'),
                'type': self.section.get('name'),
                'title': content.get('title'),
                'viewNum': content.get('viewCount'),
                'commentNum': content.get('commentCount'),
                'latestCommentTime': formatTimestamp(content.get('latestCommentTime')),
                'publishedAt': content.get('contributeTimeFormat'),
                'publishedBy': content.get('userId'),
                'bananaNum': content.get('bananaCount'),
                'contentType': self.section_type,
                'channelId': self.section['channelId']
            }

    def get_one_page_contents(self, page_number):
        if self.section_type == contentTypes['article']:
            params = {
                'pageNo': page_number,
                'size': self.page_size,
                'realmIds': self.section.get('realmIds'),
                'originalOnly': 'false',
                'orderType': self.article_order_type,
                'periodType': -1,
                'filterTitleImage': 'true',
            }
            res = Proxy().request_acfun(
                'get',
                'http://webapi.aixifan.com/query/article/list',
                params=params,
                Referer="http://www.acfun.cn/v/list{}/index.htm".format(self.section.get('channelId'))
            )

        if self.section_type == contentTypes['video']:
            params = {
                'pageNo': page_number,
                'size': 20,  # 视频默认20，传其他值也是无效的
                'channelId': self.section.get('channelId'),
                'sort': 0,
            }
            res = Proxy().request_acfun(
                'get',
                'http://www.acfun.cn/list/getlist',
                params=params,
                Referer="http://www.acfun.cn/v/list{}/index.htm".format(self.section.get('channelId'))
            )

        json = res.json()
        content_list = []
        # return正常值
        if self.section_type == contentTypes['article']:
            content_list = json.get('data').get('articleList')
        if self.section_type == contentTypes['video']:
            content_list = json.get('data').get('data')
        if len(content_list) == 0:
            print(res.json())
            print(params)
        return [self.format_content_to_model(content) for content in content_list]

    def get_contents(self):
        content_list = []
        for page_number in range(1, self.total_page + 1):
            new_content_list = self.get_one_page_contents(page_number)
            content_list.extend(new_content_list)
            if len(new_content_list) == 0:
                print(new_content_list)
                print(page_number)

            if self.min_published_date is not None:
                last_content = new_content_list[-1]
                if arrow.get(last_content['publishedAt']) < arrow.get(self.min_published_date):
                    return content_list

            if self.min_latest_comment_time is not None:
                last_content = new_content_list[-1]
                if arrow.get(last_content['latestCommentTime']) < arrow.get(self.min_latest_comment_time):
                    return content_list
        return content_list

    def save_contents(self, contents):
        session = Session()
        content_ids = {content['id'] for content in contents}
        contents_in_db = session.query(Content.id).filter(Content.id.in_(content_ids)).all()
        content_ids_in_db = {content.id for content in contents_in_db}

        need_to_save_content_ids = content_ids - content_ids_in_db
        need_to_save_contents = list(filter(lambda a: a['id'] in need_to_save_content_ids, contents))
        session.add_all([Content(**content) for content in need_to_save_contents])
        session.commit()

        session.close()

    def crawl_contents(self):
        start = time()
        start_get_time = time()

        content_list = self.get_contents()
        time_of_get = time() - start_get_time

        start_save_time = time()
        self.save_contents(content_list)
        time_of_save = time() - start_save_time

        time_of_total = time() - start
        logging.info(
            '抓取' + self.section_type + '[' + self.section.get('name') + ']分区内容' +
            '[一共抓取' + str(len(content_list)) + '个内容]' +
            '[一共花费' + str(time_of_total) + ' 秒]' +
            '[请求数据花费' + str(time_of_get) + '秒]' +
            '[处理并保存数据花费' + str(time_of_save) + '秒]'
        )
        return content_list


class CrawlOneSection(threading.Thread):
    def __init__(self, **kwargs):
        self.content_list = []
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        self.content_list = ContentSpider(**self.kwargs).crawl_contents()

    def get_result(self):
        return self.content_list


def crawl_all_sections_articles(sections, **kwargs):
    thread_list = []
    start = time()
    for section in sections:
        t = CrawlOneSection(
            section=section,
            section_type=contentTypes['article'],
            ** kwargs
        )
        t.start()
        thread_list.append(t)
    content_list = []
    for t in thread_list:
        t.join()
        content_list.extend(t.get_result())
    logging.info('此次抓取文章共使用：' + str(time() - start) + '秒')
    return content_list


def crawl_all_sections_videos(sections, **kwargs):
    thread_list = []
    start = time()
    for section in sections:
        if 'subSections' not in section:
            t = CrawlOneSection(
                section=section,
                section_type=contentTypes['video'],
                **kwargs
            )
            t.start()
            thread_list.append(t)
        else:
            sub_sections = section['subSections']
            for sub_section in sub_sections:
                t = CrawlOneSection(
                    section=section,
                    section_type=contentTypes['video'],
                    **kwargs
                )
                t.start()
                thread_list.append(t)
    content_list = []
    for t in thread_list:
        t.join()
        content_list.extend(t.get_result())
    logging.info('此次抓取视频共使用：' + str(time() - start) + '秒')
    return content_list
