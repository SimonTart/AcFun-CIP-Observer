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
observer_info_logger = logging.getLogger('observer_info_logging')
observer_error_logger = logging.getLogger('observer_error_logging')


class ContentSpider:
    def __init__(
        self,
        section,
        section_type,
        total_page=100,
        page_size=100,
        article_order_type=2,
        min_published_date=None,
        is_get_latest_comment=False
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
        self.is_get_latest_comment = is_get_latest_comment

    def format_content_to_model(self, content):
        if self.section_type == contentTypes['article']:
            return {
                'id': int(content.get('id')),
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
            if self.is_get_latest_comment:
                return {
                    'id': int(content.get('contentId')),
                    'title': content.get('title'),
                    'viewNum': content.get('views'),
                    'commentNum': content.get('comments'),
                    'publishedAt': formatTimestamp(content.get('releaseDate')),
                    'publishedBy': content.get('user').get('userId'),
                    'contentType': self.section_type,
                    'channelId': content['channelId']
                }
            else:
                return {
                    'id': int(content.get('id')),
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
        res = None
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
            if self.is_get_latest_comment is True:
                headers = {
                    'Accept': 'application/json',
                    'deviceType': '2',
                    'Origin': 'http://m.acfun.cn',
                    'productId': '2000',
                    'Referer': 'http://m.acfun.cn/list/',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
                }

                params = {
                    'pageNo': page_number,
                    'pageSize': 50,  # 最多50，超过50无效
                    'channelIds': self.section.get('channelId'),
                    'sort': 0,
                }
                res = Proxy().request_acfun(
                    'get',
                    'http://api.aixifan.com/searches/channel',
                    params=params,
                    headers=headers
                )
            else:
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

        if self.section_type == contentTypes['article']:
            content_list = json.get('data').get('articleList')

        if self.section_type == contentTypes['video']:
            if self.is_get_latest_comment is True:
                content_list = json.get('data').get('list')
            else:
                content_list = json.get('data').get('data')

        if content_list is None or len(content_list) == 0:
            observer_error_logger.error('content list为空, res is {data}, params is {params}'.format(data=json.get('data'), params=params))

        return [self.format_content_to_model(content) for content in content_list]

    def get_contents(self):
        content_list = []
        need_crawl_comment_contents = []
        for page_number in range(1, self.total_page + 1):
            new_content_list = self.get_one_page_contents(page_number)
            content_list.extend(new_content_list)
            if len(new_content_list) == 0:
                observer_error_logger.error('获取到的新content list为空，参数 page_number = {page_number}, section {section}'.format(page_number=page_number, section=self.section))
                continue

            if self.min_published_date is not None:
                observer_info_logger.debug('抓取{min_published_date}之前的文章'.format(min_published_date=self.min_published_date))
                last_content = new_content_list[-1]
                if arrow.get(last_content['publishedAt']) < arrow.get(self.min_published_date):
                    return content_list, need_crawl_comment_contents

            if self.is_get_latest_comment is True:
                observer_info_logger.debug('抓取最新评论的的文章'.format(min_published_date=self.min_published_date))
                is_need_continue, need_crawl_contents = self.is_all_comment_crawled(new_content_list)
                need_crawl_comment_contents.extend(need_crawl_contents)
                if is_need_continue is False:
                    return content_list, need_crawl_comment_contents
        return content_list, need_crawl_comment_contents

    def is_all_comment_crawled(self, contents):
        session = Session()
        content_ids = {content['id'] for content in contents}
        contents_in_db = session.query(Content.id, Content.commentNum).filter(Content.id.in_(content_ids)).all()
        contents_in_db_dict = {}
        for c in contents_in_db:
            contents_in_db_dict[c[0]] = {'id': c[0], 'commentNum': c[1]}

        need_crawl_comment_contents = []
        for content in contents:
            content_in_db = contents_in_db_dict.get(content['id'])
            comment_num_in_db = 0 if content_in_db is None else content_in_db.get('commentNum')
            if content['commentNum'] > 0 and content['commentNum'] == comment_num_in_db:
                observer_info_logger.debug('数量等于数据库的数量，终止往下爬取。抓取的内容数量{content_num},数据库的数量{db_num},内容id为{content_id}'.format(content_num=content['commentNum'],db_num=comment_num_in_db,content_id=content['id']))
                return False, need_crawl_comment_contents
            else:
                if content['commentNum'] > 0:
                    observer_info_logger.debug('把内容添加到待抓取列表中，content_id为{content_id}'.format(content_id=content['id']))
                    need_crawl_comment_contents.append(content)
        observer_info_logger.debug('继续向下抓取最新评论的文章')
        return True, need_crawl_comment_contents




    def save_contents(self, contents):
        session = Session()
        content_ids = {content['id'] for content in contents}
        contents_in_db = session.query(Content.id).filter(Content.id.in_(content_ids)).all()
        content_ids_in_db = {content.id for content in contents_in_db}

        need_to_add_content_ids = content_ids - content_ids_in_db
        need_to_add_contents = list(filter(lambda a: a['id'] in need_to_add_content_ids, contents))
        observer_info_logger.debug('添加数据库content, contentIds={content_ids}'.format(content_ids=need_to_add_content_ids))
        session.add_all([Content(**content) for content in need_to_add_contents])
        session.commit()

        need_to_update_contents = list(filter(lambda a: a['id'] in content_ids_in_db, contents))
        for content in need_to_update_contents:
            observer_info_logger.debug('更新数据库content, content={content}'.format(content=content))
            session.query(Content).filter(Content.id == content.get('id')).update({
                'commentNum': content.get('commentNum'),
                'viewNum': content.get('viewNum')
            })
        session.close()

    def crawl_contents(self):
        start = time()

        content_list, _ = self.get_contents()
        self.save_contents(content_list)

        time_of_total = time() - start
        observer_info_logger.info(
            '抓取' + self.section_type + '[' + self.section.get('name') + ']分区内容' +
            '[一共抓取' + str(len(content_list)) + '个内容]' +
            '[一共花费' + str(time_of_total) + ' 秒]'
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
        if 'subSection' not in section:
            t = CrawlOneSection(
                section=section,
                section_type=contentTypes['article'],
                **kwargs
            )
            t.start()
            thread_list.append(t)
        else:
            for subSection in sections['subSection']:
                t = CrawlOneSection(
                    section=subSection,
                    section_type=contentTypes['article'],
                    **kwargs
                )
                t.start()
                thread_list.append(t)

    content_list = []
    for t in thread_list:
        t.join()
        content_list.extend(t.get_result())
    observer_info_logger.info('此次抓取文章共使用：' + str(time() - start) + '秒')
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
                    section=sub_section,
                    section_type=contentTypes['video'],
                    **kwargs
                )
                t.start()
                thread_list.append(t)
    content_list = []
    for t in thread_list:
        t.join()
        content_list.extend(t.get_result())
    observer_info_logger.info('此次抓取视频共使用：' + str(time() - start) + '秒')
    return content_list
