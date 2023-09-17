import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestDbDdel(object):
    """
    数据资源模块，删除资源
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_1007_dba_del.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("数据库资源“删除”功能正常")
    # @allure.story("数据资源")
    def test_dba_del(self, data):
        """
        数据资源状态打开测试
        :return:
        """
        with allure.step("#1.添加要删除的资源"):
            dbadd = AddDbaBusiness().add_dba(**data)
            assert dbadd["message"] == "接口调用成功"
        with allure.step("#2.删除数据资源操作"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            dba = DbaDelInterface().dba_del(dbaid)
            assert dba["message"] == "接口调用成功"
        with allure.step("#3.检查是都删除成功"):
            br = DbaGetIdInterface().dba_dbname_if(data)
            print(br)
            assert br == True
