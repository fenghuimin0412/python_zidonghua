# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec


class StrategySetFace(object):
    """
    对策略模板的编辑：添加、修改、删除
    """

    def __init__(self):
        # 添加策略模板
        self.url = base_url + "/core/strategy/saveStrategyModel"
        # 策略模板编辑
        self.url1 = base_url + "/core/strategy/editStrategyModel"
        # 策略模板strategyId查询
        self.url2 = base_url + "/core/strategy/findStrategyPage"
        # 策略模板删除
        self.url3 = base_url + "/core/strategy/deleteStrategyModel"
        # 策略模板批量应用
        self.url4 = base_url + ""
        self.method = "post"

    # 添加策略模板
    def request_strategy(self, strategyname):
        header = {
            "Authorization": token_sec
        }
        json = {
            "strategyName": strategyname,
            "strategyExplain": "",
            "ruleIdList": [
                393,
                394,
                395,
                396,
                397,
                398,
                399,
                400
            ]
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 编辑策略组
    def request_strategy_edit(self, StrategyName, NewStrategyName):
        header = {
            "Authorization": token_sec
        }
        strategyId = self.request_find_strategy(StrategyName)
        json = {
            "strategyId": strategyId,
            "strategyName": NewStrategyName,
            "strategyExplain": "",
            "ruleIdList": [
                393,
                394,
                395,
                396,
                397,
                398,
                399,
                400
            ]
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url1,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

        # 查询策略模板 strategyId

    def request_find_strategy(self, strategyname):
        header = {
            "Authorization": token_sec
        }
        json = {
            "pageNo": 1,
            "pageSize": 30
        }
        res = requests.request(url=self.url2,
                               method=self.method,
                               json=json,
                               headers=header,
                               verify=False).json()
        if res["data"]["data"] is None:
            return 0
        strategylist = res["data"]["data"]
        strategyId = 0
        b = 0
        while b < len(strategylist):
            if strategylist[b]["strategyName"] == strategyname:
                strategyId = strategylist[b]["strategyId"]
            b = b + 1
        return strategyId

    # 删除策略模板
    def request_del_strategy(self, strategyname=None):
        strategyId = self.request_find_strategy(strategyname)
        header = {
            "Authorization": token_sec
        }
        json = {
                  "strategyId": strategyId
                }

        res = requests.request(url=self.url3,
                               method=self.method,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res


if __name__ == '__main__':
    # # 添加规则模板
    # res = StrategySetFace().request_strategy("StrategySetFace")
    # print(res)
    # # 编辑策略模板
    # res = StrategySetFace().request_strategy_edit("strategy_add", "StrategySetFace")
    # print(res)
    # 查询策略模板ID
    res = StrategySetFace().request_find_strategy("strategy_add")
    print(res)
    # 删除策略模板
    # res = StrategySetFace().request_del_strategy("StrategySetFace")
    # print(res)
