import sys
import requests
import logging
from sentry import ravenClient

def getProxy():
    proxy = requests.get('http://127.0.0.1:5010/get').text
    return proxy

def deleteProxy(proxy):
    requests.get('http://127.0.0.1:5010/delete?proxy={}'.format(proxy))

def getProxyStatus():
    return requests.get('http://127.0.0.1:5010/get_status').content


def request(method, url, **kwargs):
    requestCount = 5
    proxyCount = 20
    proxy = getProxy()
    while proxyCount > 0:
        proxy = getProxy()
        try:
            res = requests.request(method, url, timeout = 30, proxies={'http': 'http://{}'.format(proxy)}, **kwargs)
            if res.status_code == 200 or res.status_code == 304 or res.status_code == 503:
                return res
        except:
            logging.error('IP {} Not Availble'.format(proxy))
            deleteProxy(proxy)
            

    logging.error('Proxy Not Availble', extra = getProxyStatus())
    logging.info('Proxy Not Availble, Using Local Network')
    ravenClient.captureMessage('Proxy Not Availble, Using Local Network')
    return requests.request(method, url, **kwargs)

def get(url, **kwargs):
    return request('get', url, **kwargs)