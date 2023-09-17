import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestDbaAdd(object):
    """
    数据资源模块
    """

    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1003_dba_add.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    # test_data = test_data[0]
    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("正常数据，添加数据库资源正常测试")
    # @allure.story("添加数据库资源")
    def test_dba_add(self, data):
        """
        添加数据资源测试
        :param data: 读取test_dba-add.yaml添加资源的信息
        :return:
        """
        # data = data[0]
        # print(data)

        if DbaGetIdInterface().dba_dbname_if(data) is True:
            with allure.step("#1.添加mysql资源"):
                dbadd = AddDbaBusiness().add_dba(**data)
                # print(dbadd)
            with allure.step("#2.获取添加资源的报文，查看是否成功"):
                # print(dbadd)
                # sleep(1)
                assert dbadd["message"] == "接口调用成功"
        with allure.step("#a.数据资源存在无需添加"):
            print("数据资源存在无需添加")
