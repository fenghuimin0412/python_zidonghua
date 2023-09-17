# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec
# from interface.dba.dba_getid_interface import DbaQueryBusiness


class DbaSwitchBusiness(object):
    """
    资产状态开关
    """

    # 启用单个资产
    def dba_start(self, ids):
        self.url = base_url + "/2017/dbengine/start"
        self.method = "post"
        header = {
            "token": token_sec
        }
        data = {
            # "MIME Type": "application/x-www-form-urlencoded",
            "engineId": ids
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, data))
        res = requests.request(url=self.url,
                               method=self.method,
                               data=data,
                               headers=header,
                               verify=False).json()
        if "errorCode" in res.keys():
            if "数据格式错误" in res["errorCode"]:
                logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 禁用单个资产
    def dba_stop(self, ids):
        self.url = base_url + "/2017/dbengine/stop"
        self.method = "post"
        header = {
            "token": token_sec
        }
        data = {
            # "MIME Type": "application/x-www-form-urlencoded",
            "engineId": ids
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, data))
        res = requests.request(url=self.url,
                               method=self.method,
                               data=data,
                               headers=header,
                               verify=False).json()
        if "errorCode" in res.keys():
            if "数据格式错误" in res["errorCode"]:
                logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # # 禁用所有资产
    # def dba_stop_all(self):
    #     dbas = DbaQueryBusiness().dba_list()
    #     a = 0
    #     while a < len(dbas):
    #         self.dba_stop(dbas[a])
    #         a = a + 1
    #     print("禁用当前系统所有资产操作结束")
    #     return dbas
    #
    # # 启用所有资产
    # def dba_strt_all(self):
    #     dbas = DbaQueryBusiness().dba_list()
    #     # print(dbas)
    #     a = 0
    #     while a < len(dbas):
    #         self.dba_start(dbas[a])
    #         a = a + 1
    #     print("启用当前系统所有资产操作结束")
    #     return dbas
    #
    # # 启用指定段资产
    # def dba_strt_num(self, a, b):
    #     if a == None or b == None:
    #         print("输入参数不正确")
    #     if a >= 1 and b != 0 and type(eval(a)) == int and type(eval(b)) == int and a < b:
    #         while a <= b:
    #             self.dba_start(a)
    #             a = a + 1
    #
    # # 禁用指定段资产
    # def dba_stop_num(self, a, b):
    #     if a == None or b == None:
    #         print("输入参数不正确")
    #     if a >= 1 and b != 0 and type(eval(a)) == int and type(eval(b)) == int and a < b:
    #         while a <= b:
    #             self.dba_stop(a)
    #             a = a + 1
    #

# if __name__ == '__main__':
#     DbaSwitchBusiness().dba_strt_num(None, 2)

