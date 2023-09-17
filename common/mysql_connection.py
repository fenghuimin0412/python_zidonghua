import pymysql


class MysqlConnection:

    def connection(self, host=None, user=None, password=None, database=None, port=None):
        try:
            db = pymysql.connect(host=host, user=user, password=password, database=database,
                                 charset="utf8")
            print(db)
            cursor = db.cursor()  # 使用cursor（）方法获取游标
            cursor.execute("select * from test_rjy.test")  # 执行sql查询语句
            result = cursor.fetchall()  # 记录查询结果
            cursor.close()  # 关闭游标
            db.close()  # 关闭数据库连接
            print(result)  # 返回查询结果
            return "连接成功"
        except:
            return "连接失败"


if __name__ == '__main__':
    print(MysqlConnection().connection())
