# coding=utf-8

import requests
import urllib3
from cffi.backend_ctypes import long

from common.common_config import logger, base_url
from common.timeStamp import timeStamp
from common.token_str import token_sec
from instance.audlog import Audlog
from instance.dba import Dba


class AuditLogInterface(object):
    """
    检索日志
    """

    def __init__(self):
        self.url = base_url + "/core/auditlog/searchSqlAuditLog"
        self.method = "post"

        # self._response = self.request()

    # 获取当前时间前15秒的审计日志
    def request(self, audlog: Audlog):
        header = {
            "Authorization": token_sec
        }
        # 获取当前时间戳
        timestamp = timeStamp().timeStamp()
        b = int(timestamp) - 12000

        json = {
            "pageNo": 1,
            "pageSize": 30,
            "captureTimeBegin": long(b),
            "captureTimeEnd": long(timestamp),
            "condition": {
                "sqlRequestContent": {
                    "operatorCode": 1,
                    "collections": [
                        audlog.sqlRequestContent  # sql语句
                    ]
                }
            }
        }

        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))

        # if len(res["data"]["data"]) == 0:
        #     ress = "10秒内没有包含" + audlog.sqlRequestContent + "日志"
        #     return ress
        return res

    # 获取当前时间前10秒的阻断日志
    def request_find_zudaun_log(self):
        header = {
            "Authorization": token_sec
        }
        # 获取当前时间戳
        timestamp = timeStamp().timeStamp()
        b = int(timestamp) - 12000

        json = {
                  "pageNo": 1,
                  "pageSize": 10,
                  "captureTimeBegin": long(b),
                  "captureTimeEnd": long(timestamp),
                  "condition": {
                    "action": {
                      "operatorCode": 1,
                      "collections": [
                        3
                      ]
                    }
                  }
                }
        # a = {
        #     "pageNo": 1,
        #     "pageSize": 30,
        #     "captureTimeBegin": long(b),
        #     "captureTimeEnd": long(timestamp),
        # }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method="post",
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        if len(res["data"]["data"]) == 0:
            return "10秒内没有息日志"
        return res

    # 获取当前时间前10秒的高风险通过
    def request_find_gfx_tg_log(self):
            header = {
                "Authorization": token_sec
            }
            # 获取当前时间戳
            timestamp = timeStamp().timeStamp()
            b = int(timestamp) - 12000

            json = {
                  "pageNo": 1,
                  "pageSize": 30,
                  "riskLevelList": [
                    3
                  ],
                  "captureTimeBegin": long(b),
                  "captureTimeEnd": long(timestamp),
                  "condition": {
                    "action": {
                      "operatorCode": 1,
                      "collections": [
                        1
                      ]
                    }
                  }
                }
            # a = {
            #     "pageNo": 1,
            #     "pageSize": 30,
            #     "captureTimeBegin": long(b),
            #     "captureTimeEnd": long(timestamp),
            # }

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.info("{}接口的请求数据为{}".format(__name__, json))
            res = requests.request(url=self.url,
                                   method="post",
                                   # data=data,
                                   json=json,
                                   headers=header,
                                   verify=False).json()
            # if "errorCode" in res.keys():
            #     if "数据格式错误" in res["errorCode"]:
            #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
            if len(res["data"]["data"]) == 0:
                return "10秒内没有息日志"
            return res



if __name__ == '__main__':
    # # 查询 10秒内是否有存在select id from test_rjy.test 的日志
    # ab = Audlog()
    # ab.sqlRequestContent = "select id from test_rjy.test"
    # res = AuditLogInterface().request(ab)
    # print(res)
    # # timestamp = timeStamp().timeStamp()
    # # print(timestamp)

    # # 查询 10秒内所有阻断最新日志
    # res = AuditLogInterface().request_find_zudaun_log()
    # print(res)
    # # timestamp = timeStamp().timeStamp()
    # # print(timestamp)

    # 查询 10秒内所有告警-通过的日志
    res = AuditLogInterface().request_find_gfx_tg_log()
    print(res)
    # timestamp = timeStamp().timeStamp()
    # print(timestamp)
