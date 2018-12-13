from ..proxy import Proxy
import logging
import time
import arrow
from db import Session
from ..models.comment import Comment
from ..models.spiderRecord import SpiderRecord
from .content import ContentSpider
from config import contentTypes
from common.constant import record_types
import threading

observer_info_logger = logging.getLogger('observer_info_logging')
observer_error_logger = logging.getLogger('observer_error_logging')


class CommentSpider:
    def __init__(
        self,
        content_id,
        page_size=50,
        crawl_all=None,
        min_comment_time=None
    ):
        self.content_id = content_id
        self.page_size = page_size
        self.crawl_all = crawl_all
        self.min_comment_time = min_comment_time

    def request_comments(self, page_number):
        params = {
            'isNeedAllCount': 'true',
            'isReaderOnlyUpUser': 'false',
            'isAscOrder': 'false',
            'contentId': self.content_id,
            'currentPage': page_number,
            'pageSize': self.page_size,
        }
        res = Proxy().request_acfun(
            'get',
            'http://www.acfun.cn/comment_list_json.aspx',
            params=params,
            Referer='http://www.acfun.cn/a/ac{}'.format(self.content_id)
        )
        data = res.json().get('data')
        comment_list = data.get('commentList')
        if comment_list is None or len(comment_list) == 0 or data.get('commentContentArr') is None:
            observer_error_logger.error(
                'comment list为空, res is {data}, params is {params}'.format(data=data, params=params))
            return {}, [], 1
        return data.get('commentContentArr'), data.get('commentList'), data.get('totalPage')

    def get_comments_by_order(self):
        comment_dict, comment_list, total_page = self.request_comments(page_number=1)

        # 只有一页直接返回
        if total_page is 1:
            return comment_dict.values()

        # 如果要抓取全部的评论
        if self.crawl_all is True:
            for page_number in range(2, int(total_page) + 1):
                new_comment_dict, comment_list, _ = self.request_comments(page_number=page_number)
                comment_dict.update(new_comment_dict)
            return comment_dict.values()

        # 如果要抓取某个时间范围内的评论
        if self.min_comment_time is not None:
            # 异常处理
            if len(comment_list) == 0:
                return comment_dict.values()
            last_comment_id = comment_list[-1]
            last_comment_date = comment_dict.get('c' + str(int(last_comment_id))).get('postDate')
            # 第一页已经超过了，直接返回
            if arrow.get(last_comment_date) < arrow.get(self.min_comment_time):
                return comment_dict.values()

            # 继续遍历
            for page_number in range(2, int(total_page) + 1):
                new_comment_dict, new_comment_list, _ = self.request_comments(page_number=page_number)
                comment_dict.update(new_comment_dict)
                # 异常处理
                if len(comment_list) == 0:
                    continue

                last_comment_id = new_comment_list[-1]
                last_comment_date = new_comment_dict.get('c' + str(int(last_comment_id))).get('postDate')
                if arrow.get(last_comment_date) < arrow.get(self.min_comment_time):
                    return comment_dict.values()

            return comment_dict.values()

        raise Exception('获取评论出错')

    def format_comment_to_model(self, comment):
        return {
            'id': comment.get('cid'),
            'content': comment.get('content'),
            'userId': comment.get('userID'),
            'postDate': comment.get('postDate'),
            'quoteId': comment.get('quoteId'),
            'isDelete': comment.get('isDelete'),
            'isUpDelete': comment.get('isUpDelete'),
            'count': comment.get('count'),
            'refCount': comment.get('refCount'),
            'contentId': self.content_id,
        }

    def save_comments(self, comments):
        session = Session()
        comment_ids = {comment['id'] for comment in comments}
        comments_in_db = session.query(Comment.id).filter(Comment.id.in_(comment_ids)).all()
        comment_ids_in_db = {comment.id for comment in comments_in_db}
        if comment_ids_in_db is None:
            comment_ids_in_db = []
        comment_ids_in_db = set(comment_ids_in_db)

        # 添加新的评论
        need_add_comment_ids = comment_ids - comment_ids_in_db
        need_add_comments = list(filter(lambda c: c['id'] in need_add_comment_ids, comments))
        session.add_all([Comment(**comment) for comment in need_add_comments])

        # 更新旧的评论
        need_update_comments = list(
            filter(lambda c: c['id'] in comment_ids_in_db and (c['isDelete'] is True or c['isUpDelete'] is True),
                   comments))
        for comment in need_update_comments:
            db_comment = session.query(Comment).filter(Comment.id == comment.get('id'))
            db_comment.isDelete = comment.get('isDelete')
            db_comment.isUpDelete = comment.get('isUpDelete')
            session.commit()
        session.commit()
        session.close()

    def crawl_comments(self):
        comments = self.get_comments_by_order()
        comments = [self.format_comment_to_model(comment) for comment in comments]
        self.save_comments(comments)
        return comments


def crawl_latest_comments_by_contents(contents, min_comment_time):
    for content in contents:
        CommentSpider(
            content_id=content['id'],
            min_comment_time=min_comment_time
        ).crawl_comments()


def crawl_content_latest_comments(section, section_type):
    start_time = time.time()

    channel_id = section.get('channelId')
    record_type = record_types['crawl_content_comment']
    session = Session()

    spider_record = session.query(SpiderRecord).filter(
        SpiderRecord.channelId == channel_id,
        SpiderRecord.type == record_type
    ).first()

    last_success_date = arrow.now().shift(hours=-1) if spider_record is None else arrow.get(spider_record.successDate)
    kwargs = {}
    if section_type == contentTypes['article']:
        kwargs = {
            'article_order_type': 1,
            'is_get_latest_comment': True
        }

    if section_type == contentTypes['video']:
        kwargs = {
            'is_get_latest_comment': True
        }

    content_spider = ContentSpider(section, section_type, **kwargs)
    content_list, need_crawl_comment_contents = content_spider.get_contents()

    observer_info_logger.info('{section_name}需要抓取评论的内容个数为{num}'.format(num=len(need_crawl_comment_contents),
                                                                       section_name=section.get('name')))
    content_len = len(need_crawl_comment_contents)
    threads = []
    step = 20
    for start in range(0, content_len, step):
        end = start + step if start + step <= content_len else content_len
        t = threading.Thread(target=crawl_latest_comments_by_contents, args=(need_crawl_comment_contents[start:end], last_success_date))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if spider_record is None:
        session.add(SpiderRecord(
            channelId=channel_id,
            type=record_type,
            successDate=arrow.now().format('YYYY-MM-DD HH:mm:ss')
        ))
    else:
        spider_record.successDate = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    session.commit()
    session.close()
    content_spider.save_contents(content_list)
    observer_info_logger.info(
        '{section_name}抓取完成，总共花费{cost}秒'.format(cost=str(time.time() - start_time), section_name=section.get('name')))
