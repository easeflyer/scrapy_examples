# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
# -*- coding:utf-8-*-
from .proxy import GetIp, counter
from scrapy import log

ipports_dict = GetIp().get_ipport_list()


class ProxyMiddleware(object):
    http_n = 0  # counter for http requests
    https_n = 0  # counter for https requests

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        if request.url.startswith("http://"):
            n = ProxyMiddleware.http_n
            n = n if n < len(ipports_dict['http']) else 0
            request.meta['proxy'] = "%s" % (ipports_dict['http'][n])
            log.msg('Squence of http %d - %s' % (n, str(ipports_dict['http'][n])))
            ProxyMiddleware.http_n = n + 1

        if request.url.startswith("https://"):
            n = ProxyMiddleware.https_n
            n = n if n < len(ipports_dict['https']) else 0
            request.meta['proxy'] = "%s" % (ipports_dict['https'][n])
            log.msg('Squence of https %d - %s' % (n, str(ipports_dict['https'][n])))
            ProxyMiddleware.https_n = n + 1
