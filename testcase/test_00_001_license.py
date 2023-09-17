import os
from time import sleep

import allure
import pytest
from interface.system.empower import Empower



@allure.epic("数据库防火墙")
@allure.feature("系统管理-证书")
class Testcasesys(object):
    """
    数据资源模块
    """
    # testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2007_scene_qiaojie.yaml")
    # test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.license
    # @pytest.mark.parametrize("data", test_data)
    @allure.title("为被测系统证书授权")
    # @allure.story("")
    def test_sys01(self):
        """
        测试被测系统授权
        :return:
        """
        if Empower().request_find_license() is False:
            with allure.step("#授权被测系统"):
                res = Empower().request_install()
                print(res)
                assert res["msg"] == "操作成功"
        if Empower().request_find_license() is True:
            with allure.step("#授权已授权"):
                print("授权已授权")
