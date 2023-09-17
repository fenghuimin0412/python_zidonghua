import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from instance import dba
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from interface.rule.Intelligent_protection_set import IntelligentProtectionFace
from interface.rule.rule_set import RuleAddInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestJixian(object):
    """
    智能基线添加
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_3001_jixian_add.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("智能基线生成测试")
    # @allure.story("")
    def test_01(self, data):
        """
        智能基线生成测试
        :return:
        """
        if IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"]) != 0:
            with allure.step("#a.删除智能基线操作"):
                res = IntelligentProtectionFace().request_del_jixian(data["sourceName"], data["jixianName"])
                assert res["data"] == "success"
        with allure.step("#1.生成智能基线操作"):
            res = IntelligentProtectionFace().request_generate(data["sourceName"], data["jixianName"])
            assert res["data"] == "success"
        with allure.step("#2.检查是否生成基线成功"):
            res = IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"])
            assert res != 0


