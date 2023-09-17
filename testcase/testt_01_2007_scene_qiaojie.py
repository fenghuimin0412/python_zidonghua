import os
from time import sleep

import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from common.dblink.mysql_link import dbMysql
from common.mysql_connection import MysqlConnection
from instance.audlog import Audlog
from instance.mysql import Mysql
from interface.auditlog_query import AuditLogInterface
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from interface.system.network_set import NetworkSet
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理-场景")
class TestSceneDaili(object):
    """
    数据资源模块
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2007_scene_qiaojie.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("配置桥接资源，连接有日志")
    # @allure.story("数据资源")
    def test_scene01(self, data):
        """
        测试旁路配置是否正常
        :return:
        """
        # 判断如果没有该数据资源，则添加
        # dba = DbaGetIdInterface().dba_dbname_if(data)
        # if dba:
        #     with allure.step("#1.添加操作的数据资源"):
        #         dba = AddDbaBusiness().add_dba(**data)
        #         assert dba["message"] == "接口调用成功"
        #         # sleep(2)
        # with allure.step("#1.配置enp12s0和enp13s0网卡桥接"):
        #     res = NetworkSet().request_add_qj(data["enp1"], data["enp2"])
        #     assert res["message"] == "接口调用成功"
        #     sleep(8)
        # with allure.step("#2.为桥接网卡加IP"):
        #     res = NetworkSet().request_set_network(data["enp3"], data["ip_net"])
        #     assert res["message"] == "接口调用成功"
        # with allure.step("#3.先关闭资源状态"):
        #     dbaid = DbaGetIdInterface().dba_dbname_getid(data)
        #     res = SetModifyStatus().request(dbaid, 0)
        #     assert res["message"] == "接口调用成功"
        # with allure.step("#4.部署桥接资源"):
        #     dbaid = DbaGetIdInterface().dba_dbname_getid(data)
        #     res = AddDailiDeployment().request_qiaojie(dbaid)
        #     assert res["message"] == "接口调用成功"
        # #     sleep(2)
        # with allure.step("#5.打开资源状态"):
        #     dbaid = DbaGetIdInterface().dba_dbname_getid(data)
        #     res = SetModifyStatus().request(dbaid, 1)
        #     assert res["message"] == "接口调用成功"
        #     #等待后台配置生效
        #     sleep(5)
        with allure.step("#6.连接桥接资源，执行sql语句"):
            mysql = Mysql()
            mysql.host = "192.168.2.55"
            mysql.user = "root"
            mysql.password = "123456"
            mysql.database = "test"
            mysql.port = 13306
            conn = dbMysql(mysql)
            results = conn.query("select 123")
            # print(results)
            conn.close()
            assert results is not None
            # sleep(8)
        # with allure.step("#7.获取最新10秒内日志，验证只生成一条数据并且sql语句为select id from test_rjy.test"):
        #     aud = Audlog()
        #     aud.sqlRequestContent = "select id from test_rjy.test"
        #     res = AuditLogInterface().request(aud)
        #     # 判断10秒内生成一条数据并且sql语句为select id from test_rjy.test
        #     # print(res)
        #     assert len(res["data"]["data"]) == 1 and res["data"]["data"][0]["sqlPattern"] == "select id from test.test"
        # #
        #
