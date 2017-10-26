import urllib.request, urllib.error, urllib.parse
import pdb
import socket
import random

from bioon.settings import DBKWARGS
from .handledb import exec_sql
from .ipadd import IPPOOL_BACKUP_HTTP, IPPOOL_BACKUP_HTTPS

kwargs = DBKWARGS

URLS = [
    r"http://ip.chinaz.com/getip.aspx",
    r'http://httpbin.org/ip',
    r'http://python.org/',
]


def counter(start_at=0):
    '''Function: count number
	Usage: f=counter(i) print f() #i+1'''
    count = [start_at]

    def incr():
        count[0] += 1
        return count[0]

    return incr


def use_proxy(browser, proxy, url):
    '''Open browser with proxy'''
    # After visited transfer ip
    profile = browser.profile
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', proxy[0])
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    profile.set_preference('permissions.default.image', 2)
    profile.update_preferences()
    browser.profile = profile
    browser.get(url)
    browser.implicitly_wait(30)
    return browser


class Singleton(object):
    '''Signal instance example.'''

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class GetIp(Singleton):
    def __init__(self):
        sql = '''SELECT  `ip`,`port`,`type`
        FROM  `ips`
        WHERE `type`='{}'
        ORDER BY `speed` ASC
        LIMIT 25 '''
        http_sql = sql.format('HTTP')
        https_sql = sql.format('HTTPS')
        print("http_sql:{}".format(http_sql))
        print("https_sql:{}".format(https_sql))
        http_rs = exec_sql(http_sql, **kwargs)
        self.result = http_rs
        https_rs = exec_sql(https_sql, **kwargs)
        self.result.extend(https_rs)

    def del_ip(self, record):
        '''delete ip that can not use'''
        sql = "delete from ips where ip='%s' and port='%s'" % (record['ip'], record['port'])
        print(sql)
        exec_sql(sql, **kwargs)
        print(record, " was deleted.")

    def get_ipport_list(self):
        print("Proxy getip was executed.")
        if self.result:
            validated_proxy_http, validated_proxy_https, outdated = validateIp(self.result)
            print("validated_proxy_http:{}, validated_proxy_https:{}".format(len(validated_proxy_http),
                                                                             len(validated_proxy_https)))
            if outdated:
                [self.del_ip(item) for item in outdated]
            if not validated_proxy_http:
                validated_proxy_http = IPPOOL_BACKUP_HTTP
            if not validated_proxy_https:
                validated_proxy_https = IPPOOL_BACKUP_HTTPS
            return {"http": validated_proxy_http, "https": validated_proxy_https}
        return None


def validateIp(proxy):
    socket.setdefaulttimeout(3)
    validated_proxy_http = []
    validated_proxy_https = []
    outdated = []
    for i in range(0, len(proxy)):
        ip = proxy[i]['ip']
        port = proxy[i]['port']
        type = proxy[i]['type'].lower()
        proxy_ip_port = type + '://' + ip + ":" + port
        url_ = URLS[random.randint(0, len(URLS) - 1)]
        try:
            _get_data_withproxy(url_, type=type, proxy_ip_port=proxy_ip_port, data=None)
            validated_proxy_http.append(ip + ":" + port) if type == 'http' else validated_proxy_https.append(
                ip + ":" + port)
        except Exception as e:
            outdated.append(proxy[i])
            continue
    return validated_proxy_http, validated_proxy_https, outdated


def _get_data_withproxy(url, type='http', proxy_ip_port=None, data=None):
    proxy = urllib.request.ProxyHandler({type: proxy_ip_port})  # 设置proxy
    opener = urllib.request.build_opener(proxy)  # 挂载opener
    urllib.request.install_opener(opener)  # 安装opener
    if data:
        data = urllib.parse.urlencode(data).encode('utf-8')
        page = opener.open(url, data).read()
    else:
        page = opener.open(url).read()
    page = page.decode('utf-8')
    return page
