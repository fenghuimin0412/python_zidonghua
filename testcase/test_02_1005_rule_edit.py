import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.rule.rule_set import RuleAddInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRules(object):
    """
    安全策略自定义策略编辑
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_1005_rule_edit.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_rules
    @pytest.mark.parametrize("data", test_data)
    @allure.title("规则定义-自定义规则编辑测试")
    # @allure.story("数据资源")
    def test_01(self, data):
        """
        添加规则
        :return:
        """
        # 如果没有要修改的规则组则添加，如果没有修改的规则添加
        if RuleAddInterface().request_findrules(data["rulesName"]) == 0:
            with allure.step("#a.如果没有要编辑规则规则组，则添加规则组"):
                res = RuleAddInterface().request_rules(data["rulesName"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = RuleAddInterface().request_findrules(data["rulesName"])
                assert res != 0
        if RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"]) == 0:
            with allure.step("#b.如果没有要修改的规则，则添加规则"):
                res = RuleAddInterface().request_rule(data["rulesName"], data["name"], data["ruleName"], data["vlue"])
                assert res["data"] == "success"
            with allure.step("#c.检查是否添加成功"):
                res = RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"])
                assert res != 0
        # 如果有名字为rule2的规则需要删除
        if RuleAddInterface().request_findrule(data["rulesName"], data["newRuleName"]) != 0:
            with allure.step("#e.删除规则rule2"):
                res = RuleAddInterface().request_del_rule(data["rulesName"], data["newRuleName"])
                print(res)
                assert res["data"] == "success"
            with allure.step("#f.删除rule2是否成功检查"):
                res = RuleAddInterface().request_findrule(data["rulesName"], data["newRuleName"])
                assert res == 0

        with allure.step("#1.修改自定义规则名rule1为rule2"):
            res = RuleAddInterface().request_rule_edit(rulesname=data["rulesName"], rulename=data["ruleName"],
                                                       newrulesname=data["newRuleName"])
            # print(res)
            assert res["data"] == "success"
            print(res)
        with allure.step("#2.查询规则名是否被修改"):
            res = RuleAddInterface().request_findrule(data["rulesName"], data["newRuleName"])
            assert res != 0
