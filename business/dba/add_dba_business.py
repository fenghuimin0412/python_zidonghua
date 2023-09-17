# coding=utf-8
import json
import os

from secsmart_autotest.lib.util.yaml_util import YamlUtil

from common.common_config import logger
from interface.dba.add_dba import AddDbaInterface
from instance.dba import Dba
from util.get_path import DATA_DIR


class AddDbaBusiness(object):
    """
    数据库资源管理模块
    """

    def add_dba(self, **kwargs):
        dba = Dba()
        # logger.info("{}获取到的用例数据为{}".format(__name__, kwargs))
        if "databaseName" in kwargs.keys():
            dba.databaseName = kwargs["databaseName"]
        if "databaseType" in kwargs.keys():
            dba.databaseType = kwargs["databaseType"]
        if "host" in kwargs.keys():
            dba.host = kwargs["host"]
        if "port" in kwargs.keys():
            dba.port = kwargs["port"]
        if "dbName" in kwargs.keys():
            dba.dbName = kwargs["dbName"]
        if "userName" in kwargs.keys():
            dba.userName = kwargs["userName"]
        if "password" in kwargs.keys():
            dba.password = kwargs["password"]
        if "otherInfo" in kwargs.keys():
            dba.otherInfo = kwargs["otherInfo"]
        add_dba_inter = AddDbaInterface().request(dba)
        res = add_dba_inter
        logger.info("{}返回的数据为{}".format(__name__, res))
        return res

# # 调试脚本
# if __name__ == "__main__":
#     ab = AddDbaBusiness()
#     testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1003_dba_add.yaml")
#     test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]
#     # print(test_data)
#     # print(test_data[0])
#     test_data = test_data[0]
#     # da = {
#     #     "databaseName": "123567878787878",
#     #     "databaseType": 3,
#     #     "host": "192.168.1.11",
#     #     "port": "3306",
#     #     "dbName": "",
#     #     "userName": "",
#     #     "password": "",
#     #     "otherInfo": None
#     #     # "otherInfo": "{\"serverType\":0,\"assistedLogin\":false}"
#     # }
#
#     res = ab.add_dba(**test_data)
#     print(res)
