import os
from asyncio import sleep

import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from interface.rule.strategy_set import StrategySetFace
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestStrategy(object):
    """
    策略模板编辑
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_2002_strategy_edit.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_strategy
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略模板修改测试_名字")
    # @allure.story("")
    def test_01(self, data):
        """
        策略模板修改：后期维护修改更多内容
        :return:
        """

        if StrategySetFace().request_find_strategy(data["strategyNames"]) == 0:
            with allure.step("#a.如果没有要修改的策略模板，则添策略模板"):
                res = StrategySetFace().request_strategy(data["strategyNames"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = StrategySetFace().request_find_strategy(data["strategyNames"])
                assert res != 0
        sleep(2)
        with allure.step("#1.修改策略模板的名字保存"):
            res = StrategySetFace().request_strategy_edit(data["strategyNames"], data["newStrategyNames"])
            assert res["message"] == "接口调用成功"
        with allure.step("#2.修改策略模板名字是否成功检查"):
            res = StrategySetFace().request_find_strategy(data["newStrategyNames"])
            assert res != 0


