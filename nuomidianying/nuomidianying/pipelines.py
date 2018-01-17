# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .settings import DB,DB_HOST,DB_PORT,TABLE
from pymongo import MongoClient

class NuomidianyingPipeline(object):
    def process_item(self, item, spider):
        return item

class SavenuomiPipeline(object):
    def process_item(self,item,spider):
        client = MongoClient(DB_HOST,DB_PORT)
        db = client[DB]
        table = db[TABLE]
        table.insert(dict(item))

        return item