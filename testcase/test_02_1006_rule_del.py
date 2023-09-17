import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.rule.rule_set import RuleAddInterface
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRules(object):

    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_1006_rule_del.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_rules
    @pytest.mark.parametrize("data", test_data)
    @allure.title("规则定义-自定义规则删除")
    # @allure.story("数据资源")
    def test_01(self, data):
        """
        删除策略组
        :return:
        """
        if RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"]) == 0:
            with allure.step("#a.如果没有要删除规则规则组，则添加规则组"):
                res = RuleAddInterface().request_rule(data["rulesName"], data["name"], data["ruleName"], data["vlue"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"])
                assert res != 0
        # 删除规则
        with allure.step("#1.删除规则"):
            res = RuleAddInterface().request_del_rule(data["rulesName"], data["ruleName"])
            print(res)
            assert res["data"] == "success"
        with allure.step("#2.删除是否成功检查"):
            res = RuleAddInterface().request_findrule(data["rulesName"],data["ruleName"])
            assert res == 0
