import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestDbaSetDeployment(object):
    """
    数据资源模块,设置资源部署模式
    """

    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1004_dba_set_deployment.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    # test_data = test_data[0]
    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("数据库资源部署代理模式功能正常")
    # @allure.story("数据资源")
    def test_dba_set_deployment(self, data):
        """
        数据资源添加部署代理模式，端口10000测试
        :return:
        """
        with allure.step("#a.先将资源状态关闭"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            res = SetModifyStatus().request(dbaid, 0)
        with allure.step("#1.为mysql添加代理10000端口"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            res = AddDailiDeployment().request(dbaid, data["dport"])
        with allure.step("#2.获取添加的报文，查看是否成功"):
            assert res["message"] == "接口调用成功"
