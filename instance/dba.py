#coding=utf-8
class Dba(object):
    """
    dba类，描述数据库相关接口
    """

    def __init__(self,
                 databaseName="",
                 databaseType="",
                 dbName="",
                 host="",
                 otherInfo = "",
                 password="",
                 port=3306,
                 userName=""):
        self.databaseName = databaseName
        self.databaseType = databaseType
        self.dbName = dbName
        self.host = host
        self.otherInfo = otherInfo
        self.password = password
        self.port = port
        self.userName = userName

