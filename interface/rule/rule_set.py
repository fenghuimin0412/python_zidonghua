# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec


class RuleAddInterface(object):
    """
    添加策略
    """

    def __init__(self):
        self.url = base_url + "/core/strategy/saveRuleGroup"
        self.url1 = base_url + "/core/strategy/saveRule"
        # 检索界面规则数据
        self.url2 = base_url + "/core/strategy/findWholeRuleInfo"
        # 删除规则组
        self.url3 = base_url + "/core/strategy/deleteRuleGroup"
        # 删除规则
        self.url4 = base_url + "/core/strategy/deleteRule"
        # 编辑规则组
        self.url5 = base_url + "/core/strategy/editRuleGroup"
        # 编辑规则-名字
        self.url6 = base_url + "/core/strategy/editRule"
        # 编辑规则动作
        self.url7 = base_url + "/core/strategy/editRule"

        self.method = "post"

    # 添加策略组
    def request_rules(self, rulename):
        header = {
            "Authorization": token_sec
        }
        json = {
            "ruleType": 2,
            "ruleGroupName": rulename,
            "dbNameCase": 0,
            "osUserNameCase": 0,
            "clientToolsCase": 0,
            "validStatus": 1
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
    def request_rules_edit(self, rulesname, newrulesname):
        header = {
            "Authorization": token_sec
        }
        groupid = self.request_findrules(rulesname)
        json = {
            "groupId": groupid,
            "ruleType": 2,
            "ruleGroupName": newrulesname,
            "dbNameCase": 0,
            "osUserNameCase": 0,
            "clientToolsCase": 0,
            "validStatus": 1
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url5,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

        # 查询规则组 groupId

    def request_findrules(self, rulesname=None):
        header2 = {
            "Authorization": token_sec
        }
        res = requests.request(url=self.url2,
                               method=self.method,
                               # json=json,
                               headers=header2,
                               verify=False).json()
        rulelist = res["data"][0]["ruleGroupWholeList"]
        groupid = 0
        for a in rulelist:
            if a["groupName"] == rulesname:
                groupid = a["groupId"]
        return groupid

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
                if a["resultDTOList"] != None:
                    for b in a["resultDTOList"]:
                        if b["detailRuleName"] == ruleName:
                            ruleId = b["ruleId"]
        return ruleId

    # 添加规则
    # rulesname=要添加规则组的名字,name = 规则的类型,ruleneme=要添加的规则名字,value=规则的值
    def request_rule(self, rulesName=None, name=None, ruleneme=None, value=None):
        groupid = self.request_findrules(rulesName)
        header = {
            "Authorization": token_sec
        }
        json = {
            "detailRuleName": ruleneme,
            "riskLevel": 3,
            "action": 1,
            "basedOn": 1,
            "recordStatus": 4,
            "resultStatus": 0,
            "selfStatus": 1,
            "ruleParamDTOList": [
                {
                    "name": name,
                    "matchType": 1,
                    "valueSource": 1,
                    "valueList": [
                        {
                            "valueId": 1,
                            "value": value
                        }
                    ]
                }
            ],
            "groupId": groupid
        }
        # json = {
        #     "detailRuleName": ruleneme,
        #     "riskLevel": 3,
        #     "action": 1,
        #     "basedOn": 1,
        #     "recordStatus": 4,
        #     "resultStatus": 0,
        #     "selfStatus": 1,
        #     "ruleParamDTOList": [
        #         {
        #             "name": name,
        #             "matchType": 1,
        #             "valueSource": 1,
        #             "valueList": [
        #                 {
        #                     "valueId": 1,
        #                     "value": value
        #                 }
        #             ]
        #         }
        #     ],
        #     "groupId": groupid
        # }

        res = requests.request(url=self.url1,
                               method=self.method,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 编辑规则-名字
    # rulesname=要修改的规则组的名字,rulename = 要修改的规则名字,newrulesname=要修改为的新名字
    def request_rule_edit(self, rulesname=None, rulename=None, newrulesname=None):
        header = {
            "Authorization": token_sec
        }
        ruleId = self.request_findrule(rulesname, rulename)
        # print(ruleId)
        json = {
            "ruleId": ruleId,
            "detailRuleName": newrulesname,
            "riskLevel": 3,
            "action": 1,
            # "basedOn": null,
            # "lockedTime": null,
            "recordStatus": 4,
            "resultStatus": 0,
            "priority": ruleId,
            "selfStatus": 1,
            "paramList": {
                "pageNum": 1,
                "pageSize": 30,
                "totalPage": 1,
                "totalCount": 1,
                "data": [
                    {
                        "detailRuleId": ruleId,
                        "paramId": 3243,
                        "name": "table",
                        "match_type": 1,
                        "valueSource": 1,
                        "value": [
                            {
                                "valueId": 2469,
                                "value": "test"
                            }
                        ]
                    }
                ],
                # "totalLogCount": null
            },
            # "level": null,
            "ruleParamDTOList": [
                {
                    "name": "table",
                    "matchType": 1,
                    "valueSource": 1,
                    "valueList": [
                        {
                            "valueId": 2469,
                            "value": "test"
                        }
                    ]
                }
            ]
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url6,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 编辑规则-名字
    # rulesname=要修改的规则组的名字,rulename = 要修改的规则名字,action= 动作：阻断放行1通过 3阻断 4锁定
    def request_rule_edit_action(self, rulesname=None, rulename=None, action=None):
        header = {
            "Authorization": token_sec
        }
        ruleId = self.request_findrule(rulesname, rulename)
        # print(ruleId)
        json = {
            "ruleId": ruleId,
            "riskLevel": 3,
            "action": action,
            "lockedTime": 0,
            "recordStatus": 4,
            "resultStatus": 0
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=self.url7,
                               method=self.method,
                               # data=data,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 删除规则组
    def request_del_rules(self, rulesname=None):
        groupid = self.request_findrules(rulesname)
        header = {
            "Authorization": token_sec
        }
        json = {
            "groupId": groupid
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

    # 删除规则
    def request_del_rule(self, rulesName=None, ruleName=None):
        header = {
            "Authorization": token_sec
        }
        ruleId = self.request_findrule(rulesName, ruleName)
        json = {
            "ruleId": ruleId
        }

        res = requests.request(url=self.url4,
                               method=self.method,
                               json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res


if __name__ == '__main__':
    # res = RuleAddInterface().request_rules("testcaserule")
    # print(res)
    # # res = RuleAddInterface().request_findrules("testcaserule")
    # print(res)
    # 添加规则
    # res = RuleAddInterface().request_rule("testcaserule", "ip","rule1", "192.168.1.96")
    # print(res)
    # res = RuleAddInterface().request_del_rules("testcaserule")
    # print(res)
    # #查询规则
    # res = RuleAddInterface().request_findrule("testcaserule","rule1")
    # print(res)
    # 删除规则组下的规则
    # res = RuleAddInterface().request_del_rule("testcaserule","rule1")
    # print(res)
    # # 修改队则组名称
    # res = RuleAddInterface().request_rules_edit("testcaserule","777")
    # print(res)
    # # # 修改队则名称
    # res = RuleAddInterface().request_rule_edit("testcaserule","rule1","rule2")
    # print(res)

    # 设置策略动作
    res = RuleAddInterface().request_rule_edit_action("testcaserule", "rule2", "3")
    print(res)
