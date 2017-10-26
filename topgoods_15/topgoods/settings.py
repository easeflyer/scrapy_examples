# -*- coding: utf-8 -*-

# Scrapy settings for topgoods_11 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'topgoods_11'

SPIDER_MODULES = ['topgoods_11.spiders']
NEWSPIDER_MODULE = 'topgoods_11.spiders'

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':301,
    }
    
LOG_FILE = "scrapy.log"
LOG_ENCODING = None