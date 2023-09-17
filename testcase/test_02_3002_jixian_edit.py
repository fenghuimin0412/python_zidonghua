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
    智能基线修改
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_3002_jixian_edit.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("智能基线修改测试_名字")
    # @allure.story("")
    def test_01(self, data):
        """
        智能基线名字修改
        """
        if IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"]) == 0:
            with allure.step("#a.生成智能基线操作"):
                res = IntelligentProtectionFace().request_generate(data["sourceName"], data["jixianName"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否生成基线成功"):
                res = IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"])
                assert res != 0
        # 如果有要修改名字的基线需要删除
        if IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["NewjixianName"]) != 0:
            with allure.step("#c.删除名字为"+data["NewjixianName"]+"的基线"):
                res = IntelligentProtectionFace().request_del_jixian(data["sourceName"], data["NewjixianName"])
                assert res["data"] == "success"
            with allure.step("#d.检查"+data["NewjixianName"]+"名字的基线是都删除成功"):
                res = IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"])
                assert res != 0
        with allure.step("#1.修改基线_名字为jixian_002"):
            res = IntelligentProtectionFace().request_edit(sourceName=data["sourceName"], name=data["jixianName"],newname=data["NewjixianName"])
            assert res["data"] == "success"
        with allure.step("#2.检查修改基线名的后的基线是否存在"):
            res = IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["NewjixianName"])
            assert res != 0


