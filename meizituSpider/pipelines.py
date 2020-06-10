# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint
from pymongo import MongoClient


class MeizituspiderPipeline(object):
    def __init__(self):
        self.db = MongoClient().meizitu

    def process_item(self, item, spider):
        data = dict(item)
        pprint(data)
        self.db.item.insert_one(data)

        image = [{"img":img} for img in data["imgs"]]
        self.db.image.insert_many(image)
        return item
