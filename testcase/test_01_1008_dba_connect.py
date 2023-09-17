import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from interface.dba.add_dba_connect import AddConnectFace
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestEdit(object):
    """
    数据资源模块，数据库测试连接
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1008_dba_connect.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("数据库资源“数据资源测试连接”功能测试")
    # @allure.story("数据资源")
    def test_dba_connect(self, data):
        """
        数据资源测试连接
        :return:
        """
        with allure.step("#1.测试连接mysql数据资源"):
            res = AddConnectFace().request_dba_connect(dbType=data["databaseType"], host=data["host"], port=data["port"], username=data["userName"],
                           password=data["password"])
            print(res)
            assert res["data"] == "连接成功"

