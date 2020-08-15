#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import os
import pymysql
import yaml
from faker import Faker

from config.prj_conf import data_path


class DataMaker:
    __data_name = "baidu_data.yml"
    __data_path = os.path.join(data_path, __data_name)

    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="abc", password="abc123456",
                                  db="abc123456",
                                  charset="utf8")

        self.cursor = self.db.cursor()

        self.faker = Faker(locale='zh_CN')

    # faker生成测试数据到yaml文件
    def faker_data_to_yaml(self):
        data_num = 10
        for data in range(data_num):
            data = [[
                self.faker.name(),

            ]]
            with open(os.path.join(self.__data_path), 'a', encoding='utf8') as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

    # faker生成测试数据到MySQL数据库
    def faker_data_to_mysql(self):
        # 这里给出表结构，如果使用已存在的表，可以不创建表。
        sql = """
        create table user(
        id int PRIMARY KEY auto_increment,
        username VARCHAR(20),   
        password VARCHAR(20),
        address VARCHAR(35) 
        )
        """
        data_num = 20
        try:
            self.cursor.execute(sql)
            for i in range(data_num):
                sql = """insert into user(username,password,address) 
                values('%s','%s','%s')""" \
                      % (self.faker.user_name(), self.faker.password(special_chars=False), self.faker.address())
                self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        self.cursor.close()
        self.db.close()

    def mysql_data_to_yaml(self):
        # SQL 查询语句
        sql = "SELECT * from bas_school limit 10"
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for res in results:
            login_name = res[0]
            login_pwd = res[2]
            data = [[
                login_name,
                login_pwd
            ]]
            with open(os.path.join(self.__data_path), 'a', encoding='utf8') as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        # 关闭数据库连接
        self.db.close()


if __name__ == '__main__':
    dm = DataMaker()
    dm.faker_data_to_yaml()
    pass
