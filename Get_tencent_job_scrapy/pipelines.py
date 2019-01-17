# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import pymysql
from pymysql import connections
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
# class GetTencentJobScrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MongoPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

        mysql_host = settings['MYSQL_HOST']
        mysql_user = settings['MYSQL_USER']
        mysql_passwd = settings['MYSQL_PASSWD']
        mysql_db = settings['MYSQL_DB']
        self.conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)  # 保存到mongodb数据库中
        # with open('tencent_job.txt', 'a', encoding='utf-8') as f:
        #     # for i in data:  # list里面有dict的数据保存到文本的方法
        #     for key, value in data.items():
        #         f.writelines(key + ':' + str(value) + ',')
        #     f.writelines(u'\n')
        # return item
        # job_name = item['Job_name']
        # job_link = item['Job_link']
        # job_kind = item['Job_kind']
        # number = item['number']
        # place = item['place']
        # pubdate = item['pubdate']
        # Job_id = self.cursor.execute(r'select count(*) from tencent_job')
        Job_id = int(item['Job_id'])
        # python插入数据到mysql的时候，无论是什么数据类型都用%s就可以了
        self.cursor.execute(r'insert into tencent_job values(%s,%s,%s,%s,%s,%s,%s)' ,[Job_id, item['Job_name'], item['Job_link'], item['Job_kind'], item['number'], item['place'], item['pubdate']])
        # self.cursor.execute(r'insert into tencent_job values(Job_id, item['Job_name'], item['Job_link'], item['Job_kind'], item['number'], item['place'], item['pubdate']))'
        self.conn.commit()
        with open('tencent_job.txt', 'a', encoding='utf-8') as f:
            # for i in data:  # list里面有dict的数据保存到文本的方法
            for key, value in data.items():
                f.writelines(key + ':' + str(value) + ',')
            f.writelines(u'\n')
        return item

    def close_conn(self, spider):
        self.conn.close()

    # def save_to_txt(self, item, spider):
    #     data = dict(item)
    #     with open('tencent_job.txt', 'a', encoding='utf-8') as f:
    #         # for i in data:  # list里面有dict的数据保存到文本的方法
    #         for key, value in data.items():
    #             f.writelines(key + ':' + str(value) + ',')
    #         f.writelines(u'\n')


# class Mysqlpipeline(object):
#
#     def __init__(self):
#         mysql_host = settings['MYSQL_HOST']
#         mysql_user = settings['MYSQL_USER']
#         mysql_passwd = settings['MYSQL_PASSWD']
#         mysql_db = settings['MYSQL_DB']
#         self.conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd,db=mysql_db)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         # print(item)
#         data = dict(item)
#         self.cursor.execute(r'insert into tencent_job(Job_name,Job_link,Job_kind,Number_people,Place,Pubdate) values(%s,%s,%s,%d,%s,%s,)',[data['Job_name'],data['Job_link'],data['Job_kind'],data['number'],data['place'],data['pubdate']])
#         self.conn.commit()
#         return item
#
#     def close_conn(self, spider):
#         self.conn.close()
