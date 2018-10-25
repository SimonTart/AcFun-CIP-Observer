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
    def format_content_to_model(selft, content, section, section_type):
        if section_type == contentTypes['article']:
            return {
                'id': content.get('id'),
                'type': content.get('channel_name'),
                'title': content.get('title'),
                'viewNum': content.get('view_count'),
                'commentNum': content.get('comment_count'),
                'realmId': content.get('realm_id'),
                'realmName': content.get('realm_name'),
                'latestCommentTime': content.get('latest_comment_time'),
                'publishedAt': formatTimestamp(content.get('contribute_time')),
                'publishedBy': content.get('user_id'),
                'bananaNum': content.get('banana_count'),
                'contentType': section_type,
                'channelId': section['channelId']
            }

        if section_type == contentTypes['video']:
            return {
                'id': content.get('id'),
                'type': section.get('name'),
                'title': content.get('title'),
                'viewNum': content.get('viewCount'),
                'commentNum': content.get('commentCount'),
                'latestCommentTime': content.get('latest_comment_time'),
                'publishedAt': content.get('contributeTimeFormat'),
                'publishedBy': content.get('userId'),
                'bananaNum': content.get('bananaCount'),
                'contentType': section_type,
                'channelId': section['channelId']
            }

    def get_one_page_contents(self, section, section_type, page_number, page_size=100, article_order_type=2):
        if section_type == contentTypes['article']:
            params = {
                'pageNo': page_number,
                'size': page_size,
                'realmIds': section.get('realmIds'),
                'originalOnly': 'false',
                'orderType': article_order_type,
                'periodType': -1,
                'filterTitleImage': 'true',
            }
            res = Proxy().request_acfun(
                'get',
                'http://webapi.aixifan.com/query/article/list',
                params=params,
                Referer="http://www.acfun.cn/v/list{}/index.htm".format(section.get('channelId'))
            )

        if section_type == contentTypes['video']:
            params = {
                'pageNo': page_number,
                'size': 20,  # 文章默认20，传其他值也是无效的
                'channelId': section.get('channelId'),
                'sort': 0,
            }
            res = Proxy().request_acfun(
                'get',
                'http://www.acfun.cn/list/getlist',
                params=params,
                Referer="http://www.acfun.cn/v/list{}/index.htm".format(section.get('channelId'))
            )

        json = res.json()
        content_list = []
        # return正常值
        if section_type == contentTypes['article']:
            content_list = json.get('data').get('articleList')
        if section_type == contentTypes['video']:
            content_list = json.get('data').get('data')
        return [self.format_content_to_model(content, section, section_type) for content in content_list]

    def get_contents(
        self,
        section,
        section_type,
        total_page,
        article_order_type=None,
        max_published_date=None,
        max_latest_comment_time=None
    ):
        content_list = []
        for page_number in range(1, total_page + 1):
            new_content_list = self.get_one_page_contents(
                section,
                section_type,
                page_number,
                article_order_type=article_order_type
            )
            content_list.extend(new_content_list)

            if max_published_date is not None:
                last_content = new_content_list[-1]
                if arrow.get(last_content['publishedAt']) < arrow.get(max_published_date):
                    return content_list

            if max_latest_comment_time is not None:
                last_content = new_content_list[-1]
                if arrow.get(last_content['latestCommentTime']) < arrow.get(max_latest_comment_time):
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

    def crawl_contents_by_section(self, section, section_type, total_page=1):
        start = time()
        start_get_time = time()

        content_list = self.get_contents(section, section_type, total_page)
        time_of_get = time() - start_get_time

        start_save_time = time()
        self.save_contents(content_list)
        time_of_save = time() - start_save_time

        time_of_total = time() - start
        logging.info(
            '抓取' + section_type + '[' + section.get('name') + ']分区内容' +
            '[一共抓取' + str(len(content_list)) + '个内容]' +
            '[一共花费' + str(time_of_total) + ' 秒]' +
            '[请求数据花费' + str(time_of_get) + '秒]' +
            '[处理并保存数据花费' + str(time_of_save) + '秒]'
        )
        return content_list

    def crawl_all_sections_articles(self, sections, total_page):
        thread_list = []
        start = time()
        for section in sections:
            t = threading.Thread(
                target=self.crawl_contents_by_section,
                args=(section, contentTypes['article'], total_page)
            )
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()
        logging.info('此次抓取文章共使用：' + str(time() - start) + '秒')

    def crawl_all_sections_videos(self, sections, total_page):
        thread_list = []
        start = time()
        for section in sections:
            if 'subSections' not in section:
                t = threading.Thread(
                    target=self.crawl_contents_by_section,
                    args=(section, contentTypes['video'], total_page)
                )
                t.start()
                thread_list.append(t)
            else:
                sub_sections = section['subSections']
                for sub_section in sub_sections:
                    t = threading.Thread(target=self.crawl_contents_by_section,
                                         args=(sub_section, contentTypes['video'], total_page))
                    t.start()
                    thread_list.append(t)

        for t in thread_list:
            t.join()
        logging.info('此次抓取视频共使用：' + str(time() - start) + '秒')
