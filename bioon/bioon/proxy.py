from .handledb import exec_sql
import urllib.request, urllib.error, urllib.parse

dbapi = "MySQLdb"

from bioon.settings import *

try:  # py3
    import pymysql

    CURSORCLASS = pymysql.cursors.DictCursor
    pymysql.install_as_MySQLdb()
except:  # py2
    import MySQLdb

    CURSORCLASS = MySQLdb.cursors.DictCursor

kwargs = dict(
    host=MYSQL_HOST,  # 读取settings中的配置
    db=MYSQL_DBNAME,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWD,
    charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
    cursorclass=CURSORCLASS,
    use_unicode=True,
)


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
        sql = "delete from ips where ip='%s' and port='%s'" % (record[0], record[1])
        print(sql)
        exec_sql(sql, **kwargs)
        print(record, " was deleted.")

    def judge_ip(self, record):
        '''Judge IP can use or not'''
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        proxy_type = record[2].lower()
        url = http_url if proxy_type == "http" else https_url
        proxy = "%s:%s" % (record[0], record[1])
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
        http = [h[0:2] for h in self.result if h[2] == "HTTP" and self.judge_ip(h)]
        https = [h[0:2] for h in self.result if h[2] == "HTTPS" and self.judge_ip(h)]
        print("Http: ", len(http), "Https: ", len(https))
        return {"http": http, "https": https}
