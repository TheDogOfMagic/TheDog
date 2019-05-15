# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os

class AnjukePipeline(object):
    filename = []
    def save_to_csv(self, item):
        out = open(os.getcwd()+'/data/' + item['province'] + '.csv', "a", newline="", encoding='utf-8')
        if item['province'] in self.filename:
            csv_writer = csv.DictWriter(out, item.keys())
            csv_writer.writerow(item)
        else:
            csv_writer = csv.DictWriter(out, item.keys())
            csv_writer.writeheader()
            csv_writer.writerow(item)
            self.filename.append(item['province'])
        out.close()

    def process_item(self, item, spider):
        self.save_to_csv(item)
        return item
