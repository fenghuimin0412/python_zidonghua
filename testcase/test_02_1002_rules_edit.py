import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from instance import dba
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from interface.rule.rule_set import RuleAddInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRules(object):
    """
    安全策略资源编辑
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_1002_rules_edit.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_rules
    @pytest.mark.parametrize("data", test_data)
    @allure.title("规则定义-策略组编辑，名字修改")
    # @allure.story("数据资源")
    def test_01(self, data):
        """
        添加策略组
        :return:
        """

        # 判断如果没有规则，则添加
        if RuleAddInterface().request_findrules(data["rulesNames"]) == 0:
            with allure.step("#a.添加规则组"):
                res = RuleAddInterface().request_rules(data["rulesNames"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = RuleAddInterface().request_findrules(data["rulesNames"])
                assert res != 0
        with allure.step("#1.编辑规则组名称"):
            res = RuleAddInterface().request_rules_edit(data["rulesNames"], data["NewRulesNames"])
            assert res["data"] == "success"
        with allure.step("#2.检查是否编辑成功"):
            res = RuleAddInterface().request_findrules(data["NewRulesNames"])
            assert res != 0
