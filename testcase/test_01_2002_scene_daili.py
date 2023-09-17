import os
from time import sleep
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from common.common_config import base_url
from business.dba.add_dba_business import AddDbaBusiness
from common.dblink.mysql_link import dbMysql
from instance.audlog import Audlog
from instance.mysql import Mysql
from interface.auditlog_query import AuditLogInterface
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from util.conf_w import ConfWrite
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestSceneDaili(object):
    """
    数据资源模块
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2002_scene_daili.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("修改代理端口，资源可正常连接测试")
    # @allure.story("数据资源")
    def test_scene01(self, data):
        """
        修改代理端口，资源可正常连接测试
        :return:
        """

        dba = DbaGetIdInterface().dba_dbname_if(data)
        print(dba)
        # 判断如果没有该数据资源，则添加
        if dba:
            with allure.step("#1.添加要修改的数据资源"):
                AddDbaBusiness().add_dba(**data)
                dbaid = DbaGetIdInterface().dba_dbname_getid(data)
                AddDailiDeployment().request(dbaid, data["dport"])
                res = SetModifyStatus().request(dbaid, 1)
                assert res["message"] == "接口调用成功"
                # 等待代理资源开启成功，代理端口启动
                sleep(8)
        with allure.step("#2.将数据资源状态关闭"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            res = SetModifyStatus().request(dbaid, 0)
            assert res["message"] == "接口调用成功"
        sleep(5)
        with allure.step("#3.修改代理端口"):
            # dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            res = AddDailiDeployment().request(dbaid, data["setport"])
            assert res["message"] == "接口调用成功"
        with allure.step("#4.将数据资源状态打开"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            res = SetModifyStatus().request(dbaid, 1)
            assert res["message"] == "接口调用成功"
        sleep(8)
        with allure.step("#5.连接代理资源，执行sql语句"):
            mysql = Mysql()
            daili_url = ConfWrite.remove_chars(base_url, "https://")
            mysql.host = daili_url
            mysql.user = data["userName"]
            mysql.password = data["password"]
            mysql.database = data["dbName"]
            mysql.port = data["setport"]
            conn = dbMysql(mysql)
            results = conn.query("select id from test_rjy.test")
            # print(results)
            conn.close()
            assert results is not None
            sleep(8)
        with allure.step("#5.获取最新10秒内日志，验证只生成一条数据并且sql语句为select id from test_rjy.test"):
            aud = Audlog()
            aud.sqlRequestContent = "select id from test_rjy.test"
            res = AuditLogInterface().request(aud)
            # 判断10秒内生成一条数据并且sql语句为select id from test_rjy.test
            print(res)
            assert len(res["data"]["data"]) == 1 and res["data"]["data"][0][
                "sqlPattern"] == "select id from test_rjy.test"
            sleep(2)
