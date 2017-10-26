# -*- coding: utf-8 -*-

# Scrapy settings for bioon project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys

# Root path of project
PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(1, PROJECT_ROOT)
print(('sys.path:{}'.format(sys.path)))

# Scrapy项目实现的bot的名字(也为项目名称)。
BOT_NAME = 'bioon'

SPIDER_MODULES = ['bioon.spiders']
NEWSPIDER_MODULE = 'bioon.spiders'

# 保存项目中启用的下载中间件及其顺序的字典。默认:: {}
DOWNLOADER_MIDDLEWARES = {
    'bioon.middlewares.ProxyMiddleware': 90,
}

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_IP = 4

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
}

ITEM_PIPELINES = {
    'bioon.pipelines.BioonPipeline': 500
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# 是否启用DNS内存缓存(DNS in-memory cache)。默认: True
DNSCACHE_ENABLED = True

# logging输出的文件名。如果为None，则使用标准错误输出(standard error)。默认: None
LOG_FILE = 'scrapy.log'

# log的最低级别。可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG。默认: 'DEBUG'
LOG_LEVEL = 'DEBUG'

# 如果为 True ，进程所有的标准输出(及错误)将会被重定向到log中。
# 例如， 执行 print 'hello' ，其将会在Scrapy log中显示。
# 默认: False
LOG_STDOUT = False

# 对单个网站进行并发请求的最大值。默认: 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Default: True ,Whether to enable the cookies middleware. If disabled, no cookies will be sent to web servers.
COOKIES_ENABLED = True

# feed settings
FEED_URI = os.path.join(PROJECT_ROOT, 'a.txt')
FEED_FORMAT = 'jsonlines'

print("FEED_URI:{}".format(FEED_URI))

LOG_ENCODING = None

##----------------------Mail settings------------------------
# Default: ’scrapy@localhost’,Sender email to use (From: header) for sending emails.
MAIL_FROM = '*********@163.com'

# Default: ’localhost’, SMTP host to use for sending emails.
MAIL_HOST = "smtp.163.com"

# Default: 25, SMTP port to use for sending emails.
MAIL_PORT = "25"

# Default: None, User to use for SMTP authentication. If disabled no SMTP authentication will be performed.
MAIL_USER = "*********@163.com"

# Default: None, Password to use for SMTP authentication, along with MAIL_USER.
MAIL_PASS = "xxxxxxxxxxxxx"

# Enforce using STARTTLS. STARTTLS is a way to take an existing insecure connection,
# and upgrade it to a secure connection using SSL/TLS.
MAIL_TLS = False

# Default: False, Enforce connecting using an SSL encrypted connection
MAIL_SSL = False

# from settings_local reload config
try:
    from .settings_local import *
except ImportError:
    pass
