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
    testdata_file = os.path.join(DATA_DIR, "../testdata/test_02_5004_rule_cof.yaml")
    test_data = YamlUtil(testdata_file).read_yaml()["case_10000"]

    @pytest.mark.smoke_jixian
    @pytest.mark.parametrize("data", test_data)
    @allure.title("策略配置_资源应用基线，执行基线内语句不命中基线策略，不产生告警日志")
    # @allure.story("")
    def test_01(self, data):
        """
        策略应用
        """
        # 如果没有要应用的智能基线则添加
        if IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"]) == 0:
            with allure.step("#a.生成智能基线操作"):
                res = IntelligentProtectionFace().request_generate(data["sourceName"], data["jixianName"])
                assert res["data"] == "success"
            with allure.step("#b.检查是否生成基线成功"):
                res = IntelligentProtectionFace().request_find_jixianid(data["sourceName"], data["jixianName"])
                assert res != 0
        # 设置策略动作
        with allure.step("#1.为数据资源应用策略模板"):
            res = RuleConfFace().request_jixian_conf(data["sourceName"], data["jixianName"])
            assert res["data"] == "success"
        # 测试连接：执行基线内语句不告警
        with allure.step("#2.访问代理资源，执行：select id from test_rjy.test"):
            ret = AddConnectFace()
            daili_url = ConfWrite.remove_chars(base_url, "https://")
            res = ret.request_connect_data(host=daili_url, user=data["user"], password=data["password"],
                                           database=data["database"], port=data["port"], strsql=data["strsql"])
            assert res != False
        with allure.step("#3.获取最新10秒内日志，检索到一条操作为：select id from test_rjy.test的审计日志"):
            aud = Audlog()
            aud.sqlRequestContent = data["strsql"]
            res = AuditLogInterface().request(aud)
            # 判断12秒内生成一条数据并且sql语句为select id from test_rjy.test
            a = 0
            ressql = "没有得到审计日志中的sql无数据"
            while a < 12:
                sleep(2)
                res1 = res = AuditLogInterface().request(aud)["data"]["data"]
                if len(res1) != 0:
                    # print(res1)
                    res = res1[0]["ruleLevels"]
                    ressql = res1[0]["sqlPattern"]
                    break
                a = a+1
            # ruleLevels =0 无风险
            assert len(res) == 0 and ressql == data["strsql"]
