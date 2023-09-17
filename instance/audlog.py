# coding=utf-8
class Audlog(object):
    """
    audlog类，描述审计日志相关接口
    """

    def __init__(self, captureTimeBegin="", captureTimeEnd="", pageNo="", pageSize="", sqlRequestContent=""):
        self.captureTimeBegin = captureTimeBegin  # 查实起始时间
        self.captureTimeEnd = captureTimeEnd  # 查询截至时间
        self.pageNo = pageNo  # 查询页数
        self.pageSize = pageSize  # 查询每页多少数
        self.sqlRequestContent = sqlRequestContent  # sql语句
