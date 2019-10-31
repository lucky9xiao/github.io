# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class WpaperPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'wall_paper',
            'charset': 'utf8',
            "cursorclass": cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql="""
                insert into wpaper(id, img_true, img_small, Avatar, Uploader, Category, Resolution, Contrast, Size, Tags) 
                values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # defer.addErrback(self.handle_error, item, spider)
        print("导入成功")

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item["img_true"], item["img_small"], item["Avatar"], item["Uploader"], item["Category"],
                                  item["Resolution"], item["Contrast"], item["Size"], item["Tags"]))

    # def handle_error(self, error, item, spider):
    #     print('='*10+"error"+'='*10)
    #     print(error)
    #     print('='*10+"error"+'='*10)

