import os
from time import sleep
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_del_interface import DbaDelInterface
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestSceneDaili(object):
    """
    数据资源模块
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2003_scene_daili.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("测试开启状态的资源不可以删除")
    # @allure.story("数据资源")
    def test_scene01(self, data):
        """
        测试开启状态的资源可以删除
        :return:
        """

        dba = DbaGetIdInterface().dba_dbname_if(data)
        print(dba)
        #判断如果没有该数据资源，则添加
        if dba:
            with allure.step("#1.添加要删除的数据资源"):
                AddDbaBusiness().add_dba(**data)
                dbaid = DbaGetIdInterface().dba_dbname_getid(data)
                AddDailiDeployment().request(dbaid, data["dport"])
                res = SetModifyStatus().request(dbaid, 1)
                assert res["message"] == "接口调用成功"
                # 等待代理资源开启成功，代理端口启动
                # sleep(8)
        with allure.step("#2.将数开启状态的据资源状态删除"):
            dbaid = DbaGetIdInterface().dba_dbname_getid(data)
            dba = DbaDelInterface().dba_del(dbaid)
            assert dba["message"] == "数据资源开启，不能删除"
        sleep(5)
        with allure.step("#3.通过名字查询数据资源是存在"):
            bur = DbaGetIdInterface().dba_dbname_if(data)
            assert bur is False
        # with allure.step("#4.测试连接代理资源失败"):
        #     bur = MysqlConnection().connection(data)
        #     assert bur == "连接失败"
        sleep(2)
