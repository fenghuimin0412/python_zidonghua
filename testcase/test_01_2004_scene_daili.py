import os
from time import sleep
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("数据资源管理")
class TestSceneDaili(object):
    """
    数据资源模块
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_01_2004_scene_daili.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_dba
    @pytest.mark.parametrize("data", test_data)
    @allure.title("没有部署模式的数据资源不能打开资源状态")
    # @allure.story("数据资源")
    def test_scene01(self, data):
        """
        测试没有部署模式的资源开启测试
        :return:
        """

        dba = DbaGetIdInterface().dba_dbname_if(data)
        #判断如果没有该数据资源，则添加
        if dba:
            with allure.step("#1.添加操作的数据资源"):
                dba = AddDbaBusiness().add_dba(**data)
                # dbaid = DbaGetIdInterface().dba_dbname_getid(data)
                assert dba["message"] == "接口调用成功"
                # 等待代理资源开启成功，代理端口启动
                sleep(2)
        # AddDailiDeployment().request(dbaid, data["dport"])
        with allure.step("#1.没有部署模式的资源，打开状态提示：请先配置部署配置"):
            dbaids = DbaGetIdInterface().dba_dbname_getid(data)
            sleep(2)
            res = SetModifyStatus().request(dbaids, 1)
            print(res)
        assert res["message"] == "请先进行部署配置"

