# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from bioon.handledb import adb_insert_data, exec_sql
from bioon.settings import DBAPI, DBKWARGS


class BioonPipeline(object):
    def process_item(self, item, spider):
        print("item:{}".format(item))
        # store data
        adb_insert_data(item, "cfda", DBAPI, **DBKWARGS)
        return item
