import sys
import requests
import logging
from sentry import ravenClient

def getProxy():
    try:
        proxy = requests.get('http://127.0.0.1:5010/get').text
        return proxy
    except:
        return getProxy()

def deleteProxy(proxy):
    requests.get('http://127.0.0.1:5010/delete?proxy={}'.format(proxy))

def getProxyStatus():
    return requests.get('http://127.0.0.1:5010/get_status').content


def request(method, url, **kwargs):
    proxyCount = 20
    proxy = getProxy()
    while proxyCount > 0:
        proxy = getProxy()
        requestCount = 3
        while requestCount > 0:
            hasException = False
            try:
                res = requests.request(method, url, timeout = 5, proxies={'http': 'http://{}'.format(proxy)}, **kwargs)
                data = res.json().get('data')
                if res.status_code == 200 and data is not None:
                    return res
                else:
                    requestCount -= 1
            except:
                requestCount -= 1
        # logging.error('IP {} Not Availble'.format(proxy))
        proxyCount -= 1
        deleteProxy(proxy)
            

    logging.error('Proxy Not Availble', extra = getProxyStatus())
    logging.info('Proxy Not Availble, Using Local Network')
    ravenClient.captureMessage('Proxy Not Availble, Using Local Network')
    return requests.request(method, url, **kwargs)

def get(url, **kwargs):
    return request('get', url, **kwargs)