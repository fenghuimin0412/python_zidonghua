# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.rule.Intelligent_protection_set import IntelligentProtectionFace
from interface.rule.strategy_set import StrategySetFace


class RuleConfFace(object):
    """
    对策略的应用：自定义、基线、模板、虚拟补丁
    """

    def __init__(self):
        # 应用策略接口
        self.url = base_url + "/core/strategy/saveStrategyConfig"
        # 检索规则组中的规则ID数据
        self.url2 = base_url + "/core/strategy/findWholeRuleInfo"
        # 策略模板应用
        self.url3 = base_url + "/core/strategy/saveStrategyApply"
        self.method = "post"

        # 通过规则组名，规则名查询 规则ID

    def request_findrule(self, rulesName=None, ruleName=None):
        header2 = {
            "Authorization": token_sec
        }
        res = requests.request(url=self.url2,
                               method=self.method,
                               headers=header2,
                               verify=False).json()
        rulelist = res["data"][0]["ruleGroupWholeList"]
        ruleId = 0
        for a in rulelist:
            if a["groupName"] == rulesName:
                if a["resultDTOList"] is not None:
                    for b in a["resultDTOList"]:
                        if b["detailRuleName"] == ruleName:
                            ruleId = b["ruleId"]
        return ruleId

    # 通过数据资源名字获取数据资源的id
    def dba_dbname_getid(self, dbaName):
        self.urlid = base_url + "/core/source/db/findAll"
        self.method = "post"
        header = {
            "Authorization": token_sec
        }
        json = {
            "page": 1,
            "pageSize": 30,
            "dataSourceName": dbaName
        }
        res = requests.request(url=self.urlid,
                               method=self.method,
                               headers=header,
                               json=json,
                               verify=False)
        if res.json()["message"] is None:
            print("参数错误")
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        # 获取字典里的 enforcePoint
        res = res.json()["data"]
        res = res["databaseConfigs"]
        res = res[0]
        dataid = res["id"]
        return dataid

    # 策略应用自定义规则
    # sourceNama数据资源,rulesName, ruleName
    def request_rule_conf(self, sourceNama, rulesName, ruleName):
        sourceId = self.dba_dbname_getid(sourceNama)
        ruleid = self.request_findrule(rulesName, ruleName)
        header = {
            "Authorization": token_sec
        }
        json = {
            "sourceId": sourceId,
            "policyChooseStatus": 0,
            "baseLineStatus": 0,
            "ruleIdList": [
                ruleid
            ],
            "virtualPatchStatus": 0,
            "recordAllStatus": 4,
            "resultStatus": 0
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=json,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 策略应用-应用策略模板规则
    # sourceNama数据资源,strategyName规则模板名
    def request_strategy_conf(self, sourceNama, strategyName):
        strategyId = StrategySetFace().request_find_strategy(strategyName)
        sourceId = self.dba_dbname_getid(sourceNama)
        header = {
            "Authorization": token_sec
        }
        json = {
                  "strategyId": strategyId,
                  "sourceId": [
                    sourceId
                  ],
                  "virtualPatchStatus": 0,
                  "recordAllStatus": 4,
                  "resultStatus": 0
                }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url3,
                               method=self.method,
                               # data=json,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 策略应用-应用基线策略
    # sourceNama数据资源,rulesName, ruleName
    def request_jixian_conf(self, sourceNama, strategyName):
            sourceId = self.dba_dbname_getid(sourceNama)
            # 通过资源名和基线名查询基线的ID
            jixianId = IntelligentProtectionFace().request_find_jixianid(sourceNama, strategyName)
            if jixianId == 0:
                return "没有找到到基线ID"
            header = {
                "Authorization": token_sec
            }
            json = {
                  "sourceId": sourceId,
                  "policyChooseStatus": 0,
                  "baseLineStatus": 1,
                  "baseLineId": jixianId,
                  "virtualPatchStatus": 0,
                  "recordAllStatus": 4,
                  "resultStatus": 0
                }

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.info("{}接口的请求数据为{}".format(__name__, json))
            res = requests.request(url=self.url,
                                   method=self.method,
                                   # data=json,
                                   json=json,
                                   headers=header,
                                   verify=False).json()
            # if "errorCode" in res.keys():
            #     if "数据格式错误" in res["errorCode"]:
            #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
            return res

    # 策略应用-虚拟补丁策略
    # sourceNama数据资源,
    def request_patch_conf(self, sourceNama):
        sourceId = self.dba_dbname_getid(sourceNama)
        if sourceId == 0:
            return "没有找到到基线ID"
        header = {
            "Authorization": token_sec
        }
        json = {
                  "sourceId": sourceId,
                  "policyChooseStatus": 0,
                  "baseLineStatus": 0,
                  "virtualPatchStatus": 1,
                  "recordAllStatus": 4,
                  "resultStatus": 0
                }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=json,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

    # 策略应用-不应用策略，不记录日志
    # sourceNama数据资源,
    def request_null_conf(self, sourceNama):
        sourceId = self.dba_dbname_getid(sourceNama)
        if sourceId == 0:
            return "没有找到到基线ID"
        header = {
            "Authorization": token_sec
        }
        json = {
              "sourceId": sourceId,
              "policyChooseStatus": 0,
              "baseLineStatus": 0,
              "virtualPatchStatus": 0,
              "recordAllStatus": 1,
              "resultStatus": 0
            }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=json,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res

    # 策略应用-不应用策略，不记录日志
    # sourceNama数据资源,
    def request_result_conf(self, sourceNama):
        sourceId = self.dba_dbname_getid(sourceNama)
        if sourceId == 0:
            return "没有找到到基线ID"
        header = {
            "Authorization": token_sec
        }
        json = {
                  "sourceId": sourceId,
                  "policyChooseStatus": 0,
                  "baseLineStatus": 0,
                  "virtualPatchStatus": 1,
                  "recordAllStatus": 4,
                  "resultStatus": 1
                }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url,
                               method=self.method,
                               # data=json,
                               json=json,
                               headers=header,
                               verify=False).json()
        return res




if __name__ == '__main__':
    # # #查询规则
    # res = RuleConfFace().request_findrule("testcaserule", "rule2")
    # print(res)

    # # 策略应用自定义规则
    # res = RuleConfFace().request_rule_conf("testMysql2", "testcaserule", "rule2")
    # print(res)

    # # 策略应用自定义规则
    # res = RuleConfFace().request_strategy_conf("testMysql2", "strategy_add")
    # print(res)

    # # 策略应用只智能基线
    # res = RuleConfFace().request_jixian_conf("testMysql2", "jixian_001")
    # print(res)

    # # 策略虚拟补丁策略
    # res = RuleConfFace().request_patch_conf("testMysql2")
    # print(res)

    # # 不应用策略，且不记录日志
    # res = RuleConfFace().request_null_conf("testMysql2")
    # print(res)

    # 不应用策略，且不记录日志
    res = RuleConfFace().request_result_conf("testMysql2")
    print(res)
