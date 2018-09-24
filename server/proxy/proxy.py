import sys
import requests
import logging
from sentry import ravenClient

def getProxy():
    try:
        proxy = requests.get('http://127.0.0.1:5010/get/').text
        return proxy
    except:
        return getProxy()

def deleteProxy(proxy):
    requests.get('http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))

def getProxyStatus():
    return requests.get('http://127.0.0.1:5010/get_status/').content


def request(method, url, Referer, **kwargs):
    proxyCount = 20
    proxy = getProxy()
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'Cookie: session_id=3589639185CF658; _did=web_5612985630A41123; uuid=df556396b4424b85ed2af9a5bc0ac956; supernova=1',
        'DNT': '1',
        'Host': 'www.acfun.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.acfun.cn/'
    }

    if Referer is not None:
        headers['Referer'] = Referer

    while proxyCount > 0:
        proxy = getProxy()
        requestCount = 3
        while requestCount > 0:
            try:
                res = requests.request(
                    method,
                    url,
                    timeout = 5,
                    headers = headers,
                    proxies = {'http': 'http://{}'.format(proxy)},
                    **kwargs
                )
                data = res.json().get('data')
                if res.status_code == 200 and data is not None:
                    return res
                else:
                    logging.error('proxy response not right:')
                    logging.error(res.status_code)
                    logging.error(res.text)
                    requestCount -= 1
            except Exception as e:
                logging.error('proxy request fail:')
                logging.error(e)
                requestCount -= 1
        logging.error('IP {} Not Availble'.format(proxy))
        proxyCount -= 1
        deleteProxy(proxy)


    logging.error('Proxy Not Availble')
    logging.info('Proxy Not Availble, Using Local Network')
    ravenClient.captureMessage('Proxy Not Availble, Using Local Network')
    return requests.request(method, url, headers = headers, **kwargs)


def get(url, **kwargs):
    return request('get', url, **kwargs)