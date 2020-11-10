# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.jobparser_hw

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == "hh":
            salary_fn = self.salary("hh", item)
            item["source"] = 'hh.ru'

        else:
            salary_fn = self.salary("sj", item)
            item["source"] = 'superjob'

        item['salary_min'] = salary_fn[0]
        item['salary_max'] = salary_fn[1]
        item['currency'] = salary_fn[2]

        collection.insert_one(item)
        return item

    def salary(self, site, item):

        if site == "hh":

            if item["salary"][0] == "от ":
                salary_max = None
                salary_min = int(re.sub("\D", "", item["salary"][1]))
                currency = item["salary"][-2]

            elif item["salary"][0] == "до ":
                salary_max = int(re.sub("\D", "", item["salary"][1]))
                salary_min = None
                currency = item["salary"][-2]

            elif len(item["salary"]) == 7:
                salary_max = int(re.sub("\D", "", item["salary"][3]))
                salary_min = int(re.sub("\D", "", item["salary"][1]))
                currency = item["salary"][-2]

            else:
                salary_min = None
                salary_max = None
                currency = None

        else:
            salary_min = None
            salary_max = None
            currency = None

        return salary_min, salary_max, currency

    #
    #
    #
        # elif site == "sj":
