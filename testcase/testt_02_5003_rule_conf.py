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
from interface.rule.strategy_set import StrategySetFace
from util.conf_w import ConfWrite
from util.get_path import DATA_DIR


@allure.epic("数据库防火墙")
@allure.feature("安全策略")
class TestRuleCof(object):
    """
    策略应用
    """
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_5003_rule_cof.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略配置_资源应用策略模板，命中策略策略告警-高风险的测试")
    # @allure.story("")
    def test_01(self, data):
        """
        策略应用
        """
        # 如果没有要应用的策略模板则添加
        if StrategySetFace().request_find_strategy(data["strategyNames"]) == 0:
            with allure.step("#a.如果没有要应用的策略模板，则添策略模板"):
                res = StrategySetFace().request_strategy(data["strategyNames"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否添加成功"):
                res = StrategySetFace().request_find_strategy(data["strategyNames"])
                assert res != 0
        # 设置策略动作
        with allure.step("#1.为数据资源应用策略模板"):
            # 策略模板应用
            res = RuleConfFace().request_strategy_conf(data["sourceName"], data["strategyNames"])
            assert res["data"] == "success"

        # 连接数据资源，访问内置策略（命中模板规则）执行：ALTER DATABASE testmysql CHARACTER SET utf8mb4;
        with allure.step("#3.连接数据资源访问："+data["strsql"]+"语句，被阻断验证"):
            ret = AddConnectFace()
            daili_url = ConfWrite.remove_chars(base_url, "https://")
            res = ret.request_connect_data(host=daili_url, user=data["user"], password=data["password"],
                                           database=data["database"], port=data["port"], strsql=data["strsql"])
            assert res == False
        with allure.step("#4.获取最新10秒内日志，验证检索到了：高风险。动作为：通过的告警日志"):
            # 查询 12秒每两秒查询一次
            a = 0
            while a < 12:
                sleep(2)
                res1 = AuditLogInterface().request_find_gfx_tg_log()
                if res1 != "10秒内没有息日志":
                    res = res1["data"]["data"][0]["ruleLevels"][0]
                    break
                a = a+1
            # ruleLevels=[] 无风险;ruleLevels=1 低风险；ruleLevels=2中风险；ruleLevels=3高风险；ruleLevels=4致命风险
            assert int(res) == 3
