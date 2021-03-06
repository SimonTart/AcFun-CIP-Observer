import sys
import requests
import logging
from sentry import ravenClient

proxy_info_logger = logging.getLogger('proxy_info_logging')
proxy_error_logger = logging.getLogger('proxy_error_logging')


class Proxy:
    def __init__(self):
        self.MAX_GET_PROXY_TIME = 10  # 尝试获取代理的最大尝试次数
        self.currentGetProxyTime = 0  # 当前尝试获取代理的次数
        self.MAX_REQUEST_ACFUN_TIME_OF_ONE_IP = 2 # 一个IP尝试请求acfun的最大次数
        self.currentIpTryTime = 0  # 当前ip尝试的次数
        self.REQUEST_ACFUN_TIMEOUT = 2  # 请求acfun的超时设置
        self.MAX_RQUEST_ACFUN_TIME = 20  # 尝试使用最多多少个IP去请求acfun
        self.currentRequestTyIpTime = 0  # 当前请求尝试的不同ip次数
        self.REQUEST_ACFUN_HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'Cookie: session_id=3589639185CF658; _did=web_5612985630A41123; uuid=df556396b4424b85ed2af9a5bc0ac956; supernova=1',
            'DNT': '1',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.acfun.cn/'
        }

    def get_proxy(self):
        if self.currentGetProxyTime >= self.MAX_GET_PROXY_TIME:
            self.currentGetProxyTime = 0
            raise Exception('尝试获取proxy的次数超过最大限制')
        try:
            proxy = requests.get('http://127.0.0.1:5010/get/').text
            if proxy is not None and proxy != '':
                self.currentGetProxyTime = 0
                return proxy
            else:
                raise Exception('get proxy fail', proxy)
        except Exception as e:
            ravenClient.captureMessage(e, data={
                'proxy': proxy
            })
            self.currentGetProxyTime = self.currentGetProxyTime + 1;
            return self.get_proxy()

    def delete_proxy(self, proxy):
        requests.get('http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))

    def get_proxy_status(self, proxy):
        return requests.get('http://127.0.0.1:5010/get_status/').content

    def request_acfun(self, method, url, Referer=None, headers=None, **kwargs):
        if Referer is not None:
            self.REQUEST_ACFUN_HEADERS['Referer'] = Referer

        request_headers = self.REQUEST_ACFUN_HEADERS if headers is None else headers

        self.currentRequestTyIpTime = 0
        while self.currentRequestTyIpTime < self.MAX_RQUEST_ACFUN_TIME:
            proxy = self.get_proxy()
            self.currentIpTryTime = 0
            if_acfun_error = False # 是否是因为A站的原因请求失败
            if_tengine_error = False # 是否是因为是A站Tengine漏桶漏桶机制被淹没了
            while self.currentIpTryTime < self.MAX_REQUEST_ACFUN_TIME_OF_ONE_IP:
                error_res = None
                try:
                    res = requests.request(
                                method,
                                url,
                                timeout=self.REQUEST_ACFUN_TIMEOUT,
                                headers=request_headers,
                                proxies={'http': 'http://{}'.format(proxy)},
                                **kwargs
                            )
                    error_res = res
                    data = res.json().get('data')
                    if res.status_code == 200 and data is not None:
                        proxy_info_logger.info('请求acfun成功: {method} {url} {kwargs}'.format(**{
                            'method': method,
                            'url': url,
                            'kwargs': kwargs
                        }))
                        return res
                    else:
                        raise Exception('代理请求返回结果不正确：[{status_code}]'.format(**{
                            'status_code': res.status_code
                        }))
                except Exception as e:
                    proxy_error_logger.error('代理请求失败:[proxy:{proxy}]'.format(**{
                        'proxy': proxy
                    }))
                    proxy_error_logger.error(e)

                    self.currentIpTryTime = self.currentIpTryTime + 1
                    if error_res is not None:
                        text = error_res.text or '';
                        if text.find('Tengine') != -1:
                            # 被Tengine的漏斗原则给过滤了
                            if_tengine_error = True
                            self.currentIpTryTime = self.MAX_REQUEST_ACFUN_TIME_OF_ONE_IP
                            proxy_info_logger.info("因为ACFUN Tengine漏桶机制问题导致请求失败")
                        elif text.find('北京弹幕网络科技有限公司') != -1:
                            # 只是因为A站接口出问题了，返回的是500+ 或 404
                            if_acfun_error = True
                            proxy_info_logger.info("因为ACFUN接口问题导致请求失败")

                        proxy_error_logger.error(error_res.status_code)
                        proxy_error_logger.error(error_res.text)

            # 不是A站服务器原因也不是A站tengine漏桶机制过滤
            if if_acfun_error is not True and if_tengine_error is not True:
                proxy_info_logger.info("删除代理：{}".format(proxy))
                self.delete_proxy(proxy)

            self.currentRequestTyIpTime = self.currentRequestTyIpTime + 1

        proxy_error_logger.error('请求acfun失败: {method} {url} {kwargs}'.format(**{
            'method': method,
            'url': url,
            'kwargs': kwargs
        }))
        ravenClient.captureMessage('请求acfun失败, url', data={
            'method': method,
            'url': url,
            'kwargs': kwargs
        })
        raise Exception('请求acfun失败')
