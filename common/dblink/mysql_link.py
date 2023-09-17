# !/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from instance.mysql import Mysql


class dbMysql():
    '''
    pthon连接mysql数据库及对应操作
    '''

    def __init__(self, mysql: Mysql):
        # 连接数据库执行sql，port需要为整数类型的
        # self.mysql = mysql
        self.conn = pymysql.connect(host=mysql.host, port = mysql.port, user=mysql.user, password=mysql.password, database=mysql.database,
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    # 执行查询sql
    def query(self, sql):
        '''
        :param str sql: 执行的sql语句
        :return: tuple results，sql查询的结果集
        '''
        self.cursor.execute(sql)
        # 获取所有的返回结果,以元组的形式返回所有集合，每条数据是一个元组，也可以用fetchone()获取一条记录
        results = self.cursor.fetchall()
        return results

    # 执行除查询外的其他类型的sql
    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 关闭游标跟连接
    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    # 测试代码
    mysql = Mysql()
    mysql.host = '192.168.1.101'
    mysql.user = 'root'
    mysql.password = '123456'
    mysql.database = 'mysql'
    mysql.port = 12000
    conn = dbMysql(mysql)
    results = conn.query("SELECT 123")
    # results = conn.query("select id,name from auto_table where EXISTS (SELECT name from auto_table where id >15);")
    for result in results:
        print(result)
    # print(tuple(enumerate(results[0])))
    conn.close()
