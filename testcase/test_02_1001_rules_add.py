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
    安全策略资源添加
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_1001_rules_add.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_rules
    @pytest.mark.parametrize("data", test_data)
    @allure.title("规则定义-自定义策略组添加")
    # @allure.story("数据资源")
    def test_01(self, data):
        """
        添加策略组
        :return:
        """

        # 判断如果没有该数据资源，则添加
        if dba:
            with allure.step("#a.添加要删除的数据资源"):
                AddDbaBusiness().add_dba(**data)
                dbaid = DbaGetIdInterface().dba_dbname_getid(data)
                AddDailiDeployment().request(dbaid, data["dport"])
                res = SetModifyStatus().request(dbaid, 1)
                assert res["message"] == "接口调用成功"
                # 等待代理资源开启成功，代理端口启动
                # sleep(8)
            with allure.step("#b.打开数据资源状态"):
                dbaid = DbaGetIdInterface().dba_dbname_getid(data)
                res = SetModifyStatus().request(dbaid, 1)
                assert res["message"] == "接口调用成功"
        if RuleAddInterface().request_findrules(data["rulesNames"]) != 0:
            with allure.step("#c.如果有要添加的策略组存在则删除"):
                res = RuleAddInterface().request_del_rules(data["rulesNames"])
                assert res["message"] == "接口调用成功"
            with allure.step("#d.删除是否成功检查"):
                res = RuleAddInterface().request_findrules(data["rulesNames"])
                assert res == 0
        with allure.step("#1.添加规则组"):
            res = RuleAddInterface().request_rules(data["rulesNames"])
            assert res["data"] == "success"
        with allure.step("#2.检查是否添加成功"):
            res = RuleAddInterface().request_findrules(data["rulesNames"])
            assert res != 0


