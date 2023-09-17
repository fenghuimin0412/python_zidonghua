# coding=utf-8
import requests
import urllib3
from common.common_config import logger, base_url
from common.token_str import token_sec
from interface.dba.dba_getid_interface import DbaGetIdInterface


class IntelligentProtectionFace(object):
    """
    对智能基线模块的操作：添加、修改、删除
    """

    def __init__(self):
        # 生成智能基线
        self.url = base_url + "/core/baseline/geneBaseline"
        # 基线编辑
        self.url1 = base_url + "/core/baseline/editBaseline"
        # 查询基线的ID查询
        self.url2 = base_url + "/core/baseline/baselineList"
        # 智能基线删除
        self.url3 = base_url + "/core/baseline/delBaseline"
        # 基线外策略编辑
        self.url4 = base_url + "/core/baseline/editOut"
        self.method = "post"

    # 生成智能基线
    # sourcename数据资源名字 name添加基线的名字
    def request_generate(self, sourcename, name):
        header = {
            "Authorization": token_sec,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"databaseName":sourcename}
        sourceId = DbaGetIdInterface().dba_dbname_getid(data)
        name = name
        sourceId = str(sourceId)  # 数据资源ID
        # 当前默认收集5月到24年8月的基线内容
        startTime = "2023-05-31"
        startTime1 = "00:00:00"
        endTime = "2024-08-31 23:59:00"
        endTime1 = "23:59:00"

        # 拼接URL
        addurl = self.url + "?name=" + name + "&sourceId=" + sourceId + "&startTime=" + startTime + "%20" + startTime1 + "&endTime=" + endTime + "%20" + endTime1
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # logger.info("{}接口的请求数据为{}".format(__name__, json))
        res = requests.request(url=addurl,
                               method=self.method,
                               # data=json,
                               # json=json,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 编辑基线
    # sourceName数据资源名，baselineId要修改的基线名，name要修改的参数
    def request_edit(self, sourceName, name, newname):
        header = {
            "Authorization": token_sec
        }
        # 查询智能基线id
        id = self.request_find_jixianid(sourceName, name)
        # print(id)
        editurl = self.url1 + "?baselineId=" + str(id) + "&name=" + newname
        res = requests.request(url=editurl,
                               method=self.method,
                               headers=header,
                               verify=False).json()
        # # if "errorCode" in res.keys():
        # #     if "数据格式错误" in res["errorCode"]:
        # #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 查询基线 strategyId
    # sourceName资源名,name查询的基线名
    def request_find_jixianid(self, sourceName=None, name=None):
        header = {
            "Authorization": token_sec
        }
        data = {"databaseName": sourceName}
        dbaid = DbaGetIdInterface().dba_dbname_getid(data)
        findurl = self.url2 + "?sourceId=" + str(dbaid) + "&pageNum=1&pageSize=50"
        # findurl = "https://192.168.1.80/core/baseline/baselineList?sourceId=41&pageNum=1&pageSize=30"
        res = requests.request(url=findurl,
                               method="get",
                               # json=json,
                               headers=header,
                               verify=False).json()
        jixianlist = res["data"]["data"]
        jixianId = 0
        b = 0
        while b < len(jixianlist):
            if jixianlist[b]["name"] == name:
                jixianId = jixianlist[b]["id"]
            b = b + 1
        return jixianId

    # 删除智能基线
    # sourceName要删除基线的资源,jixianname要删除基线的名字
    def request_del_jixian(self, sourceName=None, jixianname=None):
        jixianId = self.request_find_jixianid(sourceName, jixianname)
        header = {
            "Authorization": token_sec
        }
        # 拼接删除URL
        delurl = self.url3 + "?baselineId=" + str(jixianId)
        res = requests.request(url=delurl,
                               method=self.method,
                               headers=header,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res

    # 基线外策略编辑
    def reques_jixianwai_edit(self):
        # jixianId=self.request_find_id(sourceName,jixianname)
        header = {
            "Authorization": token_sec,
            "Content-Type": "application/json"
        }
        data = [
            {
                "id": 2,
                "strategyId": 1,
                "action": 1,
                "threat": 1,
                "loglevel": 4,
                "sourceId": 41,
                "name": "unrecognizedDBUser",
                "nameDesc": "未识别数据库用户",
                "isEnable": "true"
            },
            {
                "id": 3,
                "strategyId": 2,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "strangeDBUser",
                "nameDesc": "陌生数据库用户",
                "isEnable": "true"
            },
            {
                "id": 4,
                "strategyId": 3,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "strangeClientIp",
                "nameDesc": "陌生客户端IP",
                "isEnable": "true"
            },
            {
                "id": 5,
                "strategyId": 4,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "strangeClient",
                "nameDesc": "陌生客户端/应用",
                "isEnable": "true"
            },
            {
                "id": 6,
                "strategyId": 5,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "strangeDB",
                "nameDesc": "陌生数据库",
                "isEnable": "true"
            },
            {
                "id": 7,
                "strategyId": 6,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "strangeTable",
                "nameDesc": "陌生表操作访问",
                "isEnable": "false"
            },
            {
                "id": 8,
                "strategyId": 7,
                "action": 1,
                "threat": 3,
                "loglevel": 4,
                "sourceId": 41,
                "name": "othersOperate",
                "nameDesc": "其他操作信息",
                "isEnable": "true"
            }
        ]
        data1 = {
            "id": 7,
            "strategyId": 6,
            "action": 1,
            "threat": 3,
            "loglevel": 4,
            "sourceId": 41,
            "name": "strangeTable",
            "nameDesc": "陌生表操作访问",
            "isEnable": "false"
        }
        res = requests.request(url=self.url4,
                               method=self.method,
                               headers=header,
                               data=data,
                               verify=False).json()
        # if "errorCode" in res.keys():
        #     if "数据格式错误" in res["errorCode"]:
        #         logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
        return res


if __name__ == '__main__':
    # # # # 生成基线
    # res = IntelligentProtectionFace().request_generate("testMysql2", "123123123")
    # print(res)

    # 通过资源名和基线名查询基线的ID
    sourceName = "testMysql2"
    name = "IntelligentProtection_set"
    res = IntelligentProtectionFace().request_find_jixianid("testMysql2", "jixian_001")
    print(res)

    # # # 编辑基线
    # sourceName="testMysql2"
    # name="jixian_001"
    # newname = "jixian_002"
    # res = IntelligentProtectionFace().request_edit(sourceName=sourceName,name=name,newname=newname)
    # print(res)

    # # 删除基线
    # sourceName = "testMysql2"
    # jixianname = "时代的"
    # res = IntelligentProtectionFace().request_del_jixian(sourceName,jixianname)
    # print(res)

    # res = IntelligentProtectionFace().reques_jixianwai_edit()
    # print(res)
