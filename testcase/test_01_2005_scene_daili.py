import os
from time import sleep
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.dba.dba_getid_interface import DbaGetIdInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestSceneDaili(object):
    """
    数据资源模块
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2005_scene_daili.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("通过名字可以检索到，对应的数据资源信息")
    # @allure.story("数据资源")
    def test_scene01(self, data):
        """
        测试界面查询功能
        :return:
        """

        with allure.step("#1.通过名字查询该资源"):
            dba = DbaGetIdInterface().dba_dbname_if(data)
            print(dba)
            #验证数据资源是否存在，存在返回False
            assert dba == False
            sleep(8)

