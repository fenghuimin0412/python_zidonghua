import os

import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil

from interface.login.logout import LogoutInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("登录登出")
class TestLogout(object):
    """
    退出公共模块
    """

    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1002_logout.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_1001"]

    @pytest.mark.smoke_login
    @pytest.mark.parametrize("data", test_data)
    # @allure.testcase(url="http://172.16.32.24/zentao/testcase-view-8702-1.html",
    #                  name="#8702#正常账号，正常登录")
    #@allure.testcase()
    @allure.title("正常账号，正常退出测试")
    # @allure.story("登出")
    def test_logout(self, data):
        """
        账号的退出测试
        :param data: 读取logout.yaml的用户信息
        :return:
        """
        with allure.step("#1.点击右上角用户名下的”退出“"):
            logout = LogoutInterface().request(data)
            print(logout)
            assert logout["msg"] == "退出登录"

