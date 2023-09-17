import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.login.login_bus import LoginBusiness
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("登录登出")
class TestLogin(object):
    """
    登录公共模块
    """

    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1001_login.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_1001"]

    @pytest.mark.smoke_login
    @pytest.mark.parametrize("data", test_data)
    # @allure.testcase(url="http://172.16.32.24/zentao/testcase-view-8702-1.html",
    #                  name="#8702#正常账号，正常登录")
    #@allure.testcase()
    @allure.title("正常账号，正常登录")
    # @allure.story("登录")
    def test_login(self, data):
        """
        账号的登录测试
        :param data: 读取login.yaml的用户信息
        :return:
        """
        with allure.step("#1.输入正确的账号和密码"):
            login = LoginBusiness().login(**data).json()
            # print(login.json())
        with allure.step("#2.点击登录"):
            pass
        with allure.step("#3.获取登录的报文，查看请求账号是否登录成功"):
            assert login["msg"] == "认证通过！"

    test_data = YamlUtil(testdata_file).read_yaml()["case_1002"]
    @pytest.mark.smoke
    @pytest.mark.parametrize("data", test_data)
    # @allure.testcase(url="http://172.16.32.24/zentao/testcase-view-8702-1.html",
    #                  name="#8702#正常账号，正常登录")
    # @allure.testcase()
    @allure.title("异常账号，登录失败测试")
    @allure.story("登录")
    def test_logout(self, data):
        """
        账号的退出测试
        :param data: 读取logout.yaml的用户信息
        :return:
        """
        with allure.step("#1.输入不存在账号"):
            logout = LoginBusiness().login(**data).json()
        with allure.step("#2.点击登录"):
            pass
        with allure.step("#2.点击登录"):
            assert logout["msg"] == "账号不存在！"

