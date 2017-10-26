import urllib.request, urllib.error, urllib.parse
import pdb

from bioon.settings import DBKWARGS
from .handledb import exec_sql


kwargs = DBKWARGS


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
        WHERE `type` REGEXP  'HTTP|HTTPS'
        AND  `speed`<5 OR `speed` IS NULL
        ORDER BY `type` ASC
        LIMIT 200 '''
        self.result = exec_sql(sql, **kwargs)

    def del_ip(self, record):
        '''delete ip that can not use'''
        sql = "delete from ips where ip='%s' and port='%s'" % (record['ip'], record['port'])
        print(sql)
        exec_sql(sql, **kwargs)
        print(record, " was deleted.")

    def judge_ip(self, record):
        '''Judge IP can use or not'''
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        proxy_type = record['type'].lower()
        pdb.set_trace()
        url = http_url if proxy_type == "http" else https_url
        proxy = "%s:%s" % (record['ip'], record['port'])
        try:
            req = urllib.request.Request(url=url)
            req.set_proxy(proxy, proxy_type)
            response = urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            print("Request Error:", e)
            self.del_ip(record)
            return False
        else:
            code = response.getcode()
            if code >= 200 and code < 300:
                print('Effective proxy', record)
                return True
            else:
                print('Invalide proxy', record)
                self.del_ip(record)
                return False

    def get_ips(self):
        print("Proxy getip was executed.")
        http = [h['ip'].decode('utf-8') + ':' + h['port'].decode('utf-8') for h in self.result if
                h['type'] == "HTTP" and self.judge_ip(h)]
        https = [h['ip'].decode('utf-8') + ':' + h['port'].decode('utf-8') for h in self.result if
                 h['type'] == "HTTPS" and self.judge_ip(h)]
        print("Http: ", len(http), "Https: ", len(https))
        return {"http": http, "https": https}
