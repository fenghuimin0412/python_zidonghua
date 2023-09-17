# coding=utf-8

import requests
from common.common_config import logger, base_url
from common.token_str import token_sec


class DbaGetIdInterface(object):
    """
    获取所有DBA的数据id
    """

    # 通过数据资源名字获取数据资源的id
    def dba_dbname_getid(self, data):
        self.url = base_url + "/core/source/db/findAll"
        self.method = "post"

        header = {
            "Authorization": token_sec
        }
        json = {
            "page": 1,
            "pageSize": 30,
            "dataSourceName": data["databaseName"]
        }
        res = requests.request(url=self.url,
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
    # 判断这个名字的数据资源你是否不存在
    def dba_dbname_if(self, data):
        self.url = base_url + "/core/source/db/findAll"
        self.method = "post"

        header = {
            "Authorization": token_sec
        }
        json = {
            "page": 1,
            "pageSize": 30,
            "dataSourceName": data["databaseName"]
        }
        res = requests.request(url=self.url,
                               method=self.method,
                               headers=header,
                               json=json,
                               verify=False)
        if res.json()["message"] is None:
            print("参数错误")
        # 获取字典里的 enforcePoint
        res = res.json()["data"]
        len(res["databaseConfigs"])
        if len(res["databaseConfigs"]) != 0:
            #该名字的数据资源还在
            return False
        # 该名字的数据资源没有查询到
        return True

    def dba_dbaid_list(self):  #查询所有数据资源ID
        self.url = base_url + "/core/source/db/findAll"
        self.method = "post"
        header = {
            "Authorization": token_sec
        }
        json = {
            "page": 1,
            "pageSize": 100
        }
        res = requests.request(url=self.url,
                               method=self.method,
                               headers=header,
                               json=json,
                               verify=False).json()
        dbalist = res["data"]["databaseConfigs"]
        if len(dbalist) == 0 :
            # print("没有数据资源")
            return "没有数据资源"
        # 获取字典里的 enforcePoint
        res = res["data"]["databaseConfigs"]
        a = 0
        dba_list = []
        while a < len(res):
            abd_id = res[a]["id"]
            dba_list.append(abd_id)
            a = a + 1
        return dba_list
        # # 获取字典里的 enforcePoint
        # res = res.json()["data"]
        # len(res["databaseConfigs"])
        # if len(res["databaseConfigs"]) != 0:
        #     return False
        # return res


    # # 获取所有的dba_list
    # def dba_list_dba(self):
    #     self.url = base_url + "/enforcepoint/list_v2"
    #     self.method = "get"
    #     header = {
    #         "token": token
    #     }
    #     res = requests.request(url=self.url,
    #                            method=self.method,
    #                            headers=header,
    #                            verify=False).json()
    #     if "errorCode" in res.keys():
    #         if "数据格式错误" in res["errorCode"]:
    #             logger.error("测试的接口{}参数异常，请检查参数".format(__name__))
    #     # 获取resp中的data
    #     res = res["data"]
    #     return res

    # data数据解析分离
    # def data_req(self):
    #     datas = self.dba_list_dba()
    #     data2 = []
    #     dba_list = self.dba_list()
    #     # print("55555",dba_list)
    #     i = 0
    #     while i < len(dba_list):
    #         data1 = {}
    #         data1["id"] = dba_list[i]
    #         dat = datas[i]["enforcePoint"]
    #         data1["alias"] = dat.get("alias")
    #         data1["type"] = dat.get("type")
    #         data1["ip"] = dat.get("ip")
    #         data1["port"] = dat.get("port")
    #         data1["dbName"] = dat.get("dbName")
    #         data1["isWebAuth"] = dat.get("isWebAuth")
    #         data1["isRiskscan"] = dat.get("isRiskscan")
    #         data1["isRecovery"] = dat.get("isRecovery")
    #
    #         data1["ddmUser"] = datas[i]["ddmUser"]
    #         data1["ddmPwd"] = datas[i]["ddmPwd"]
    #         data1["ddiDbId"] = datas[i]["ddiDbId"]
    #         data1["patternName"] = datas[i]["patternName"]
    #         data1["firePort"] = datas[i]["firePort"]
    #         data1["isSsl"] = datas[i]["isSsl"]
    #         data1["isDdm"] = datas[i]["isDdm"]
    #         data1["isOracleRAC"] = datas[i]["isOracleRAC"]
    #         data1["isDdi"] = datas[i]["isDdi"]
    #         data1["isTwoway"] = datas[i]["isTwoway"]
    #         data1["isFuzzy"] = datas[i]["isFuzzy"]
    #         data1["isQzblj"] = datas[i]["isQzblj"]
    #         # print(data1)
    #         data2.append(data1)
    #         del data1
    #         i = i + 1
    #         # print("最终发送给子方法的", data2)
    #     return data2


        # print("2222", dba_list)
        # b = 0
        # # i = 0
        # # while i < len(datas):
        # #     data2[i] = i
        # #     i = i+1
        # for a in dba_list:
        #     dat = datas[b]["enforcePoint"]
        #     # print("ppppppppppppppp", dat)
        #     data1["alias"] = dat.get("alias")
        #     data1["type"] = dat.get("type")
        #     data1["ip"] = dat.get("ip")
        #     data1["port"] = dat.get("port")
        #     data1["dbName"] = dat.get("dbName")
        #     data1["isWebAuth"] = dat.get("isWebAuth")
        #     data1["isRiskscan"] = dat.get("isRiskscan")
        #     data1["isRecovery"] = dat.get(dat["isRecovery"])
        #     data1["ddmUser"] = datas[b]["ddmUser"]
        #     data1["ddmPwd"] = datas[b]["ddmPwd"]
        #     data1["ddiDbId"] = datas[b]["ddiDbId"]
        #     data1["patternName"] = datas[b]["patternName"]
        #     data1["firePort"] = datas[b]["firePort"]
        #     data1["isSsl"] = datas[b]["isSsl"]
        #     data1["isDdm"] = datas[b]["isDdm"]
        #     data1["isOracleRAC"] = datas[b]["isOracleRAC"]
        #     data1["isDdi"] = datas[b]["isDdi"]
        #     data1["isTwoway"] = datas[b]["isTwoway"]
        #     data1["isFuzzy"] = datas[b]["isFuzzy"]
        #     data1["isQzblj"] = datas[b]["isQzblj"]
        #     # print(b)
        #     # print(data1)
        #     data2.append(data1)
        #     print("22222222222", data2)
        #     # data2[str(b)] = data2.update(data1)
        #     # print(data2)
        #     b = b + 1
        #     # print("最终发送给子方法的", data2)
        # print("333333333",data2)
        # return data2


if __name__ == '__main__':
    data={'databaseName': 'testMysql2'}
    # dba = DbaGetIdInterface().dba_dbname_getid(data)
    # # print(dba)
    # a =DbaGetIdInterface().dba_dbname_if(data)
    # print(a)

    a =DbaGetIdInterface().dba_dbname_getid(data)
    print(a)