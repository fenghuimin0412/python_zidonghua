import os
from time import sleep

import allure
import pytest
from secsmart_autotest.lib.util.yaml_util import YamlUtil
from business.dba.add_dba_business import AddDbaBusiness
from common.common_config import base_url
from instance import dba
from instance.audlog import Audlog
from interface.auditlog_query import AuditLogInterface
from interface.dba.add_dba_connect import AddConnectFace
from interface.dba.add_dba_deployment import AddDailiDeployment
from interface.dba.dba_getid_interface import DbaGetIdInterface
from interface.dba.set_modify_status import SetModifyStatus
from interface.rule.Intelligent_protection_set import IntelligentProtectionFace
from interface.rule.rule_conf import RuleConfFace
from interface.rule.rule_set import RuleAddInterface
from util.conf_w import ConfWrite
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRuleCof(object):
    """
    策略应用
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_5001_rule_cof.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略配置_配置自定义策略，命中策略阻断测试")
    # @allure.story("")
    def test_01(self, data):
        """
        策略应用
        """
        # 如果没有要应用的策略则添加
        if RuleAddInterface().request_findrules(data["rulesName"]) == 0:
            with allure.step("#a.如果没有要编辑规则规则组，则添加规则组"):
                res = RuleAddInterface().request_rules(data["rulesName"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = RuleAddInterface().request_findrules(data["rulesName"])
                assert res != 0
        if RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"]) == 0:
            with allure.step("#b.如果没有要应用的规则，则添加规则"):
                res = RuleAddInterface().request_rule(data["rulesName"], data["name"], data["ruleName"], data["vlue"])
                assert res["data"] == "success"
            with allure.step("#c.检查是否添加成功"):
                res = RuleAddInterface().request_findrule(data["rulesName"], data["ruleName"])
                assert res != 0
        # 设置策略动作
        with allure.step("#1.设置规则为阻断规则"):
            res = RuleAddInterface().request_rule_edit_action(data["rulesName"], data["ruleName"], "3")
            assert res["data"] == "success"
        with allure.step("#2.给"+data["sourceName"]+"数据资源应用策略"+data["rulesName"]+"下的"+data["ruleName"]):
            res = RuleConfFace().request_rule_conf(data["sourceName"], data["rulesName"], data["ruleName"])
            assert res["data"] == "success"
        # 测试连接：访问test表被阻断
        with allure.step("#3.连接数据资源访问："+data["strsql"]+"语句，被阻断验证"):
            ret = AddConnectFace()
            daili_url = ConfWrite.remove_chars(base_url, "https://")
            res = ret.request_connect_data(host=daili_url, user=data["user"], password=data["password"],
                                           database=data["database"], port=data["port"], strsql=data["strsql"])
            assert res == False
        with allure.step("#4.获取最新10秒内日志，验证只生成一条数据并且sql语句为select id from test_rjy.test"):
            # 判断10秒内生成的审计日志中有没阻断语句
            # 查询 12秒每两秒查询一次，查询阻断日志
            a = 0
            while a < 12:
                sleep(2)
                res1 = AuditLogInterface().request_find_zudaun_log()
                if res1 != "10秒内没有息日志":
                    res = res1["data"]["data"][0]["action"]
                    break
                a = a+1
            # action=3 为阻断
            assert int(res) == 3
