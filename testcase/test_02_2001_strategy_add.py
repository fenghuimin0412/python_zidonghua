import os
import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.rule.rule_set import RuleAddInterface
from interface.rule.strategy_set import StrategySetFace
from util.get_path import DATA_DIR

@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestStrategy(object):
    """
    策略模板添加
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_2001_strategy_add.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_strategy
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略模板增加测试")
    # @allure.story("数据资源")
    def test_01(self, data):
        """
        添加规则模板
        :return:
        """
        # 如果有要添加的规则，则删除
        if StrategySetFace().request_find_strategy(data["strategyNames"]) !=0:
            with allure.step("#a.如果有添加的规则模板，则删除规则模板"):
                res = StrategySetFace().request_del_strategy(data["strategyNames"])
                assert res["data"] == "success"
        with allure.step("#1.添加策略模板"):
            res = StrategySetFace().request_strategy(data["strategyNames"])
            assert res["data"] == "success"
        with allure.step("#2.添加策略模板是否成功检查"):
            res = StrategySetFace().request_find_strategy(data["strategyNames"])
            assert res != 0


