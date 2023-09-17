# coding=utf-8
class Mysql(object):
    """
    mysql类，描述数据库相关接口
    """

    def __init__(self, host="", port="", user="", password="", database=""):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
